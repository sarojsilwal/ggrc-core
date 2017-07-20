# -*- coding: utf-8 -*-

# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Integration tests for sending the notifications about WF tasks "due soon".
"""

import functools
from datetime import date, datetime

from freezegun import freeze_time
from mock import patch

import ddt

from ggrc import models
from ggrc.notifications import common

from integration.ggrc import TestCase
from integration.ggrc_workflows.generator import WorkflowsGenerator
from integration.ggrc.api_helper import Api
from integration.ggrc.generator import ObjectGenerator


@ddt.ddt
class TestTaskDueNotifications(TestCase):
  """Test suite for task due soon/today notifications."""

  # pylint: disable=invalid-name

  def _fix_notification_init(self):
    """Fix Notification object init function.

    This is a fix needed for correct created_at field when using freezgun. By
    default the created_at field is left empty and filed by database, which
    uses system time and not the fake date set by freezugun plugin. This fix
    makes sure that object created in freeze_time block has all dates set with
    the correct date and time.
    """
    def init_decorator(init):
      """"Adjust the value of the object's created_at attribute to now."""
      @functools.wraps(init)
      def new_init(self, *args, **kwargs):
        init(self, *args, **kwargs)
        if hasattr(self, "created_at"):
          self.created_at = datetime.now()
      return new_init

    models.Notification.__init__ = init_decorator(models.Notification.__init__)

  def setUp(self):
    super(TestTaskDueNotifications, self).setUp()
    self.api = Api()
    self.wf_generator = WorkflowsGenerator()
    self.object_generator = ObjectGenerator()
    models.Notification.query.delete()

    self._fix_notification_init()

    self.random_objects = self.object_generator.generate_random_objects(2)
    _, self.user = self.object_generator.generate_person(
        user_role="Administrator")

    person_dict = {
        "href": "/api/people/{}".format(self.user.id),
        "id": self.user.id,
        "type": "Person",
    }

    self.one_time_workflow = {
        "title": "one time test workflow",
        "notify_on_change": True,
        "description": "some test workflow",
        "is_verification_needed": False,
        "owners": [person_dict.copy()],
        "task_groups": [{
            "title": "one time task group",
            "contact": person_dict.copy(),
            "task_group_tasks": [{
                "title": "task 1",
                "description": "some task",
                "contact": person_dict.copy(),
                "start_date": date(2017, 5, 15),
                "end_date": date(2017, 6, 11),
            }, {
                "title": "task 2",
                "description": "some task 2",
                "contact": person_dict.copy(),
                "start_date": date(2017, 5, 8),
                "end_date": date(2017, 6, 12),
            }, {
                "title": "task 3",
                "description": "some task 3",
                "contact": person_dict.copy(),
                "start_date": date(2017, 5, 31),
                "end_date": date(2017, 6, 13),
            }, {
                "title": "task 4",
                "description": "some task 4",
                "contact": person_dict.copy(),
                "start_date": date(2017, 6, 2),
                "end_date": date(2017, 6, 14),
            }, {
                "title": "task 5",
                "description": "some task 5",
                "contact": person_dict.copy(),
                "start_date": date(2017, 6, 8),
                "end_date": date(2017, 6, 15),
            }],
            "task_group_objects": self.random_objects
        }]
    }

  @ddt.unpack
  @ddt.data(
      ("2017-06-12 12:12:12", [], []),
      ("2017-06-13 13:13:13", ["task 3"], ["task 4"]),
  )
  @patch("ggrc.notifications.common.send_email")
  def test_creating_obsolete_notifications(
      self, fake_now, expected_due_today, expected_due_in, _
  ):
    """Notifications already obsolete on creation date should not be created.
    """
    with freeze_time("2017-06-12 09:39:32"):
      tmp = self.one_time_workflow.copy()
      _, workflow = self.wf_generator.generate_workflow(tmp)
      self.wf_generator.generate_cycle(workflow)
      response, workflow = self.wf_generator.activate_workflow(workflow)
      self.assert200(response)

    user = models.Person.query.get(self.user.id)

    with freeze_time(fake_now):
      _, notif_data = common.get_daily_notifications()
      user_notifs = notif_data.get(user.email, {})

      due_today_notifs = user_notifs.get("due_today", {})
      titles = [n['title'] for n in due_today_notifs.itervalues()]
      self.assertEqual(titles, expected_due_today)

      due_in_notifs = user_notifs.get("due_in", {})
      titles = [n['title'] for n in due_in_notifs.itervalues()]
      self.assertEqual(titles, expected_due_in)
