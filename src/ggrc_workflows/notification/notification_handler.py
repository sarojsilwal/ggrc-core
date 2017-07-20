# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Handlers for workflow notifications.

This module contains all function needed for handling notification objects
needed by workflow notifications. The exposed functions are the entry points
for callback listeners.

exposed functions
    handle_workflow_modify,
    handle_cycle_task_group_object_task_put,
    handle_cycle_created,
    handle_cycle_modify,
    handle_cycle_task_status_change,
"""

from datetime import timedelta
from datetime import datetime
from datetime import date

from sqlalchemy import and_
from sqlalchemy import or_
from sqlalchemy import inspect
from sqlalchemy.sql.expression import true

from ggrc import db
from ggrc.models.notification import Notification
from ggrc.models.notification import NotificationType

from ggrc_workflows.models.cycle_task_group_object_task import \
    CycleTaskGroupObjectTask


def handle_task_group_task(obj, notif_type=None):
  """Add notification entry for task group tasks.

  Args:
    obj: Instance of a model for which the notification should be scheduled.
    notif_type: The notification type for the scheduled notification.
  """
  if not notif_type:
    return

  notification = get_notification(obj)
  if not notification:
    start_date = obj.task_group.workflow.next_cycle_start_date
    send_on = start_date - timedelta(notif_type.advance_notice)
    add_notif(obj, notif_type, send_on)


def handle_workflow_modify(sender, obj=None, src=None, service=None):
  """Update or add notifications on a workflow update."""
  if obj.status != "Active" or obj.frequency == "one_time":
    return

  if not obj.next_cycle_start_date:
    obj.next_cycle_start_date = date.today()

  notification = get_notification(obj)
  notif_type = get_notification_type(
      "{}_workflow_starts_in".format(obj.frequency))

  if not notification:
    send_on = obj.next_cycle_start_date - timedelta(notif_type.advance_notice)
    add_notif(obj, notif_type, send_on)

    notif_type = get_notification_type("cycle_start_failed")
    add_notif(obj, notif_type, obj.next_cycle_start_date + timedelta(1))

  for task_group in obj.task_groups:
    for task_group_task in task_group.task_group_tasks:
      handle_task_group_task(task_group_task, notif_type)


def add_cycle_task_due_notifications(task):
  """Add notifications entries for cycle task due dates.

  Create notification entries: one for X days before the due date, one on the
  due date, and one for the days after ta task has become overdue.

  Args:
    task: CycleTaskGroupObjectTask instance to generate the notifications for.
  """
  if task.status in task.inactive_states:
    return
  if not task.cycle_task_group.cycle.is_current:
    return

  today = date.today()

  # NOTE: when deciding whether or not to create a new notification, we require
  # the send_on date to be strictly greater than TODAY - new notifications with
  # send_on date equal to TODAY will not be sent in time, because the cron job
  # for sending notifications runs soon after midnight (1 AM?)
  #
  # Yes, there is a small time window between midnight and the time the daily
  # notifications are processed and sent, but it unlikely users will work at
  # those hours. Also, this issue is likely already affecting several other
  # existing notifications and time checks revolving around TODAY, requiring
  # a holistic approac to solving it.

  notif_type = get_notification_type("{}_cycle_task_due_in".format(
      task.cycle_task_group.cycle.workflow.frequency))
  send_on = task.end_date - timedelta(notif_type.advance_notice)
  if send_on > today:
    add_notif(task, notif_type, send_on)

  notif_type = get_notification_type("cycle_task_due_today")
  send_on = task.end_date - timedelta(notif_type.advance_notice)
  if send_on > today:
    add_notif(task, notif_type, send_on)

  notif_type = get_notification_type("cycle_task_overdue")
  send_on = task.end_date + timedelta(1)
  add_notif(task, notif_type, send_on, repeating=True)


def add_cycle_task_notifications(obj, start_notif_type=None):
  """Add start and due  notification entries for cycle tasks."""
  add_notif(obj, start_notif_type, date.today())
  add_cycle_task_due_notifications(obj)


def add_cycle_task_reassigned_notification(obj):
  """Add or update notifications for reassigned cycle tasks."""
  # check if the current assignee already got the first notification
  result = db.session.query(Notification)\
      .join(NotificationType)\
      .filter(and_(Notification.object_id == obj.id,  # noqa
                   Notification.object_type == obj.type,
                   Notification.sent_at != None,
                   or_(NotificationType.name == "cycle_task_reassigned",
                       NotificationType.name == "cycle_created",
                       NotificationType.name == "manual_cycle_created",
                       )))

  if not db.session.query(result.exists()).one()[0]:
    return

  notif_type = get_notification_type("cycle_task_reassigned")
  add_notif(obj, notif_type)


def modify_cycle_task_notification(obj, notification_name):
  notif_type = get_notification_type(notification_name)
  notif = Notification.query.filter(
      Notification.object_id == obj.id,
      Notification.object_type == obj.type,
      Notification.notification_type == notif_type,
      or_(Notification.sent_at.is_(None), Notification.repeating == true()),
  ).first()
  send_on = datetime.combine(obj.end_date, datetime.min.time()) - timedelta(
      notif_type.advance_notice)

  today = datetime.combine(date.today(), datetime.min.time())
  if send_on < today:
    # this should not be allowed, but if a cycle task is changed to a past
    # date, we remove the current pending notification if it exists
    if notif:
      db.session.delete(notif)
  elif notif:
    # when cycle date is moved in the future and current exists we update
    # the current
    notif.send_on = send_on
    db.session.add(notif)
  else:
    # when cycle date is moved in the future and no current create new
    # notification
    add_notif(obj, notif_type, send_on)


def modify_cycle_task_overdue_notification(task):
  """Add or update the task's overdue notification.

  If an overdue notification already exists for the task, its date of sending
  is adjusted as needed. If such notification does not exist yet, it gets
  created.

  Args:
    task: The CycleTaskGroupObjectTask instance for which to update the overdue
          notifications.
  """
  notif_type = get_notification_type(u"cycle_task_overdue")
  send_on = datetime.combine(task.end_date, datetime.min.time()) + timedelta(1)
  notif = Notification.query.filter(
      Notification.object_id == task.id,
      Notification.object_type == task.type,
      (Notification.sent_at.is_(None) | (Notification.repeating == true())),
      Notification.notification_type == notif_type,
  ).first()

  if notif:
    if notif.send_on != send_on:
      notif.send_on = send_on
      db.session.add(notif)
    return

  # NOTE: The "task.id" check is to assure a notification is created for
  # existing task instances only, avoiding DB errors. Overdue notifications
  # for new tasks are handled and added elsewhere.
  if all([task.id, task.status in task.active_states, task.cycle.is_current]):
    add_notif(task, notif_type, send_on, repeating=True)


def modify_cycle_task_end_date(obj):
  modify_cycle_task_notification(obj, "{}_cycle_task_due_in".format(
      obj.cycle_task_group.cycle.workflow.frequency))
  modify_cycle_task_notification(obj, "cycle_task_due_today")
  modify_cycle_task_overdue_notification(obj)


def handle_cycle_task_status_change(obj, new_status, old_status):
  if obj.status == CycleTaskGroupObjectTask.DECLINED:
    notif_type = get_notification_type("cycle_task_declined")
    add_notif(obj, notif_type)
    return

  if obj.status in obj.inactive_states:
    for notif in get_notification(obj):
      db.session.delete(notif)  # delete all notification for inactive obj
    # if all tasks are in inactive states then add notification to cycle
    if all(task.status in task.inactive_states for task in
           obj.cycle.cycle_task_group_object_tasks):
      add_notif(obj.cycle, get_notification_type("all_cycle_tasks_completed"))
    db.session.flush()
    return
  # Modify overdue notification if task is still in active state
  if new_status in obj.active_states:
    modify_cycle_task_overdue_notification(obj)


def handle_cycle_task_group_object_task_put(obj):
  if inspect(obj).attrs.contact.history.has_changes():
    add_cycle_task_reassigned_notification(obj)

  history = inspect(obj).attrs.end_date.history
  if not history.has_changes():
    return

  # NOTE: A history might "detect" a change even if end_date was not changed
  # due to different data types, i.e.  date vs. datetime with the time part set
  # to zero. Example:
  #
  #   >>> datetime(2017, 5, 15, 0, 0) == date(2017, 5, 15)
  #   False
  #
  # We thus need to manually check both date values without the time part
  # in order to avoid unnecessary work and DB updates.
  old_date = history.deleted[0] if history.deleted else None
  new_date = history.added[0] if history.added else None

  if old_date is not None and new_date is not None:
    if isinstance(old_date, datetime):
      old_date = old_date.date()
    if isinstance(new_date, datetime):
      new_date = new_date.date()

    if old_date == new_date:
      return  # we have a false positive, no change actually occurred

  # the end date has actually changed, respond accordingly
  modify_cycle_task_end_date(obj)


def handle_cycle_modify(sender, obj=None, src=None, service=None):
  if obj.is_current:
    return
  for cycle_task in obj.cycle_task_group_object_tasks:
    for notif in get_notification(cycle_task):
      db.session.delete(notif)


def handle_cycle_created(sender, obj=None, src=None, service=None,
                         manually=False):

  notification = get_notification(obj)

  if not notification:
    db.session.flush()
    notification_type = get_notification_type(
        "manual_cycle_created" if manually else "cycle_created"
    )
    add_notif(obj, notification_type)

  for cycle_task_group in obj.cycle_task_groups:
    for task in cycle_task_group.cycle_task_group_tasks:
      add_cycle_task_notifications(task, notification_type)


def get_notification(obj):
  # maybe we shouldn't return different thigs here.
  result = Notification.query.filter(
      and_(Notification.object_id == obj.id,
           Notification.object_type == obj.type,
           or_(
               Notification.sent_at.is_(None),
               Notification.repeating == true())
           )
  )
  return result.all()


def get_notification_type(name):
  return db.session.query(NotificationType).filter(
      NotificationType.name == name).first()


def add_notif(obj, notif_type, send_on=None, repeating=False):
  if not send_on:
    send_on = date.today()
  notif = Notification(
      object_id=obj.id,
      object_type=obj.type,
      notification_type=notif_type,
      send_on=send_on,
      repeating=repeating,
  )
  db.session.add(notif)
