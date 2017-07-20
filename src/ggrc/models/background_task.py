# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Module for ggrc background tasks."""

import traceback
from logging import getLogger
from functools import wraps
from time import time

from flask import request
from flask.wrappers import Response
from werkzeug.datastructures import Headers

from ggrc import db
from ggrc import settings
from ggrc.login import get_current_user
from ggrc.models.mixins import Base
from ggrc.models.deferred import deferred
from ggrc.models.mixins import Stateful
from ggrc.models.types import CompressedType


logger = getLogger(__name__)


class BackgroundTask(Base, Stateful, db.Model):
  """Background task model."""
  __tablename__ = 'background_tasks'

  VALID_STATES = [
      "Pending",
      "Running",
      "Success",
      "Failure"
  ]
  name = deferred(db.Column(db.String), 'BackgroundTask')
  parameters = deferred(db.Column(CompressedType), 'BackgroundTask')
  result = deferred(db.Column(CompressedType), 'BackgroundTask')

  _publish_attrs = [
      'name',
      'result'
  ]

  _aliases = {
      "status": {
          "display_name": "State",
          "mandatory": False,
          "description": "Options are: \n{}".format('\n'.join(VALID_STATES))
      }
  }

  def start(self):
    """Mark the current task as running."""
    self.status = "Running"
    db.session.add(self)
    db.session.commit()

  def finish(self, status, result):
    """Finish the current bg task."""
    # Ensure to not commit any not-yet-committed changes
    db.session.rollback()

    if isinstance(result, Response):
      self.result = {'content': result.response[0],
                     'status_code': result.status_code,
                     'headers': result.headers.items()}
    else:
      self.result = {'content': result,
                     'status_code': 200,
                     'headers': [('Content-Type', 'text/html')]}
    self.status = status
    db.session.add(self)
    db.session.commit()

  def make_response(self, default=None):
    """Create task status response."""
    if self.result is None:
      return default
    from ggrc.app import app
    return app.make_response((self.result['content'],
                              self.result['status_code'],
                              self.result['headers']))


def create_task(name, url, queued_callback=None, parameters=None, method=None):
  """Create a enqueue a bacground task."""
  if not method:
    method = request.method

  # task name must be unique
  if not parameters:
    parameters = {}
  task = BackgroundTask(name=name + str(int(time())))
  task.parameters = parameters
  task.modified_by = get_current_user()
  db.session.add(task)
  db.session.commit()

  # schedule a task queue
  if getattr(settings, 'APP_ENGINE', False):
    from google.appengine.api import taskqueue
    headers = Headers(request.headers)
    headers.add('x-task-id', task.id)
    taskqueue.add(
        queue_name="ggrc",
        url=url,
        name="{}_{}".format(task.name, task.id),
        params={'task_id': task.id},
        method=method,
        headers=headers
    )
  elif queued_callback:
    queued_callback(task)
  return task


def make_task_response(id_):
  """Make a response for a task with the given id."""
  task = BackgroundTask.query.get(id_)
  return task.make_response()


def queued_task(func):
  """Decorator for task queues."""
  from ggrc.app import app

  @wraps(func)
  def decorated_view(*args, **_):
    """Background task runner.

    This runner makes sure that the task is called with the task model as
    the parameter.
    """
    if args and isinstance(args[0], BackgroundTask):
      task = args[0]
    else:
      task_id = request.headers.get("X-Task-Id", request.values.get("task_id"))
      task = BackgroundTask.query.get(task_id)
    task.start()
    try:
      result = func(task)
    except:  # pylint: disable=bare-except
      # Bare except is allowed here so that we can respond with the correct
      # message to all exceptions.
      logger.exception("Task failed")
      task.finish("Failure", app.make_response((
          traceback.format_exc(), 200, [('Content-Type', 'text/html')])))

      # Return 200 so that the task is not retried
      return app.make_response((
          'failure', 200, [('Content-Type', 'text/html')]))
    task.finish("Success", result)
    return result
  return decorated_view
