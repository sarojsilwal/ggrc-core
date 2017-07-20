# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Data handlers for notifications for objects in ggrc module.

Main contributed functions are:
  get_assignable_data,
"""

import datetime
import urlparse

from collections import namedtuple
from logging import getLogger

import pytz
from pytz import timezone

from ggrc import models
from ggrc import utils
from ggrc.utils import DATE_FORMAT_US


# a helper type for storing comments' parent object information
ParentObjInfo = namedtuple(
    "ParentObjInfo", ["id", "object_type", "title", "url"])


# pylint: disable=invalid-name
logger = getLogger(__name__)


def get_object_url(obj):
  """Get url for the object info page.

  Args:
    obj (db.Model): Object for which we want to info page url.

  Returns:
    string: Url for the object info page.
  """
  # pylint: disable=protected-access
  url = "{}/{}".format(obj._inflector.table_plural, obj.id)
  return urlparse.urljoin(utils.get_url_root(), url)


def as_user_time(utc_datetime):
  """Convert a UTC time stamp to a localized user-facing string.

  Args:
    utc_datetime: naive datetime.datetime, intepreted as being in UTC

  Returns:
    A user-facing string representing the given time in a localized format.
  """
  # NOTE: For the time being, the majority of users are located in US/Pacific
  # time zone, thus the latter is used to convert UTC times read from database.
  pacific_tz = timezone("US/Pacific")
  datetime_format = DATE_FORMAT_US + " %H:%M:%S %Z"

  local_time = utc_datetime.replace(tzinfo=pytz.utc).astimezone(pacific_tz)
  return local_time.strftime(datetime_format)


def _get_assignable_dict(people, notif):
  """Get dict data for assignable object in notification.

  Args:
    people (List[Person]): List o people objects who should receive the
      notification.
    notif (Notification): Notification that should be sent.
  Returns:
    dict: dictionary containing notification data for all people in the given
      list.
  """
  obj = get_notification_object(notif)
  data = {}

  for person in people:
    # We should default to today() if no start date is found on the object.
    start_date = getattr(obj, "start_date", datetime.date.today())
    data[person.email] = {
        "user": get_person_dict(person),
        notif.notification_type.name: {
            obj.id: {
                "title": obj.title,
                "start_date_statement": utils.get_digest_date_statement(
                    start_date, "start", True),
                "url": get_object_url(obj),
                "notif_created_at": {
                    notif.id: as_user_time(notif.created_at)
                }
            }
        }
    }
  return data


def assignable_open_data(notif):
  """Get data for open assignable object.

  Args:
    notif (Notification): Notification entry for an open assignable object.

  Returns:
    A dict containing all notification data for the given notification.
  """
  obj = get_notification_object(notif)
  if not obj:
    logger.warning(
        '%s for notification %s not found.',
        notif.object_type, notif.id,
    )
    return {}
  people = [person for person, _ in obj.assignees]

  return _get_assignable_dict(people, notif)


def assignable_updated_data(notif):
  """Get data for updated assignable object.

  Args:
    notif (Notification): Notification entry for an open assignable object.

  Returns:
    A dict containing all notification data for the given notification.
  """
  obj = get_notification_object(notif)
  if not obj:
    logger.warning(
        '%s for notification %s not found.',
        notif.object_type, notif.id,
    )
    return {}
  people = [person for person, _ in obj.assignees]

  return _get_assignable_dict(people, notif)


def _get_declined_people(obj):
  """Get a list of people for declined notifications.

  Args:
    obj (Model): An assignable model

  Returns:
    A list of people that should receive a declined notification according to
    the given object type.
  """
  if obj.type == "Assessment":
    return [person for person, _ in obj.assignees]
  return []


def assignable_declined_data(notif):
  """Get data for declined assignable object.

  Args:
    notif (Notification): Notification entry for a declined assignable object.

  Returns:
    A dict containing all notification data for the given notification.
  """
  obj = get_notification_object(notif)
  people = _get_declined_people(obj)
  return _get_assignable_dict(people, notif)


def get_assessment_url(assessment):
  return urlparse.urljoin(
      utils.get_url_root(),
      "assessments/{}".format(assessment.id))


def assignable_reminder(notif):
  """Get data for assignable object for reminders"""
  obj = get_notification_object(notif)
  reminder = next((attrs for attrs in obj.REMINDERABLE_HANDLERS.values()
                   if notif.notification_type.name in attrs['reminders']),
                  False)

  notif_data = {}
  if reminder:
    data = reminder['data']
    if obj.status not in data:
      # In case object already moved out of targeted state
      return notif_data
    assignee_group = data[obj.status]
    people = [a for a, roles in obj.assignees if assignee_group in roles]

    for person in people:
      notif_data[person.email] = {
          "user": get_person_dict(person),
          notif.notification_type.name: {
              obj.id: {
                  "title": obj.title,
                  "end_date": obj.end_date.strftime("%m/%d/%Y")
                  if obj.end_date else None,
                  "url": get_assessment_url(obj)
              }
          }
      }
  return notif_data


def get_person_dict(person):
  """Return dictionary with basic person info.

  Args:
    person (Person): Person object for which we want to get a dictionary.

  Returns:
    dict: dictionary with persons email, name and id.
  """
  if person:
    return {
        "email": person.email,
        "name": person.name,
        "id": person.id,
    }

  return {"email": "", "name": "", "id": -1}


def get_notification_object(notif):
  """Get an object for which the notification entry was made.

  Args:
    notif (Notifications): Notification entry for the given object

  Returns:
    A model based on notif.object_id and notif.object_type.
  """
  model = getattr(models, notif.object_type, None)
  if model:
    return model.query.get(notif.object_id)
  return None


def get_assignable_data(notif):
  """Return data for assignable object notifications.

  Args:
    notif (Notification): notification with an Assignable object_type.

  Returns:
    Dict with all data for the assignable notification or an empty dict if the
    notification is not for a valid assignable object.
  """
  if notif.object_type not in {"Assessment"}:
    return {}

  # a map of notification type suffixes to functions that fetch data for those
  # notification types
  data_handlers = {
      "_open": assignable_open_data,
      "_started": assignable_open_data,  # reuse logic, same data needed
      "_updated": assignable_updated_data,
      "_completed": assignable_updated_data,
      "_ready_for_review": assignable_updated_data,
      "_verified": assignable_updated_data,
      "_reopened": assignable_updated_data,
      "_declined": assignable_declined_data,
      "_reminder": assignable_reminder,
  }

  notif_type = notif.notification_type.name

  for suffix, data_handler in data_handlers.iteritems():
    if notif_type.endswith(suffix):
      return data_handler(notif)

  return {}


def generate_comment_notification(obj, comment, person):
  """Prepare notification data for a comment that was posted on an object.

  Args:
    obj: the object the comment was posted on
    comment: a Comment instance
    person: the person to be notified about the comment

  Returns:
    Dictionary with data needed for the comment notification email.
  """
  parent_info = ParentObjInfo(
      obj.id,
      obj._inflector.title_singular.title(),
      obj.title,
      get_object_url(obj)
  )

  return {
      "user": get_person_dict(person),
      "comment_created": {
          parent_info: {
              comment.id: {
                  "description": comment.description,
                  "commentator": get_person_dict(comment.modified_by),
                  "parent_type": parent_info.object_type,
                  "parent_id": parent_info.id,
                  "parent_url": get_object_url(obj),
                  "parent_title": obj.title,
                  "created_at": comment.created_at,
                  "created_at_str": as_user_time(comment.created_at)
              }
          }
      }
  }


def get_comment_data(notif):
  """Return data for comment notifications.

  This functions checks who should receive the notification and who not, with
  the Commentable mixin that must be added on the object which has the current
  comment. If the object on which the comment was made is not Commentable, the
  function will return an empty dict.

  Args:
    notif (Notification): notification with a Comment object_type.

  Returns:
    Dict with all data needed for sending comment notifications.
  """
  data = {}
  recipients = set()
  comment = get_notification_object(notif)
  comment_obj = None
  rel = models.Relationship.find_related(comment, models.Assessment())

  if rel:
    comment_obj = rel.Assessment_destination or rel.Assessment_source
  if not comment_obj:
    logger.warning('Comment object not found for notification %s', notif.id)
    return {}

  if comment_obj.recipients:
    recipients = set(comment_obj.recipients.split(","))

  for person, assignee_type in comment_obj.assignees:
    if not recipients or recipients.intersection(set(assignee_type)):
      data[person.email] = generate_comment_notification(
          comment_obj, comment, person)
  return data
