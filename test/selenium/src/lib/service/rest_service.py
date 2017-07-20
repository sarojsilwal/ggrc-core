# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Create and manipulate objects via REST API."""
# pylint: disable=too-few-public-methods

import json

from requests import exceptions

from lib import environment, factory
from lib.constants import url, objects, templates, messages
from lib.entities.entities_factory import ObjectPersonsFactory
from lib.service.rest.client import RestClient
from lib.utils import string_utils


class BaseRestService(object):
  """Base class for business layer's services objects."""
  def __init__(self, endpoint):
    self.endpoint = endpoint
    self.client = RestClient(self.endpoint)
    self.entities_factory_cls = factory.get_cls_entity_factory(
        object_name=self.endpoint)

  def create_list_objs(self, entity_factory, count, attrs_to_factory=None,
                       **attrs_for_template):
    """Create and return list of objects used entities factories,
    REST API service and attributes to make JSON template to request.
    As default entity factory is generating random objects,
    if 'attrs_for_factory' is not None then factory is generating objects
    according to 'attrs_for_factory' (dictionary of attributes).
    """
    list_factory_objs = [entity_factory.create() for _ in xrange(count)]
    if attrs_to_factory:
      list_factory_objs = [
          entity_factory.create(**attrs_to_factory) for _ in xrange(count)]
    list_attrs = [self.get_items_from_resp(self.client.create_object(
        **dict(factory_obj.__dict__.items() + attrs_for_template.items())))
        for factory_obj in list_factory_objs]
    return [
        self.set_obj_attrs(attrs=attrs, obj=factory_obj, **attrs_for_template)
        for attrs, factory_obj in zip(list_attrs, list_factory_objs)]

  def update_list_objs(self, entity_factory, list_objs_to_update,
                       attrs_to_factory=None, **attrs_for_template):
    """Update and return list of objects used entities factories,
    REST API service and attributes to make JSON template to request.
    As default entity factory is generating random objects,
    if 'attrs_for_factory' is not None then factory is generating objects
    according to 'attrs_for_factory' (dictionary of attributes).
    """
    list_new_objs = [entity_factory.create() for _ in
                     xrange(len(list_objs_to_update))]
    if attrs_to_factory:
      list_new_objs = [entity_factory.create(**attrs_to_factory) for _ in
                       xrange(len(list_objs_to_update))]
    list_new_attrs = [
        self.get_items_from_resp(
            self.client.update_object(
                href=old_obj.href,
                **dict({k: v for k, v in new_obj.__dict__.iteritems() if
                        k != "href"}.items() + attrs_for_template.items()))
        ) for old_obj, new_obj in zip(list_objs_to_update, list_new_objs)]
    return [self.set_obj_attrs(new_attrs, new_obj) for
            new_attrs, new_obj in zip(list_new_attrs, list_new_objs)]

  @staticmethod
  def get_items_from_resp(response):
    """Check response from server and get items {key: value} from it."""
    def get_extra_items(response):
      """Get extra items {key: value} that used in entities."""
      extra = {}
      if response.get("selfLink"):
        extra.update({"href": response.get("selfLink")})
      if response.get("viewLink"):
        extra.update(
            {"url": environment.APP_URL + response.get("viewLink")[1:]})
      return extra
    resp = json.loads(response.text)
    if response.status_code == 200:  # check response from server
      if (isinstance(resp, list) and
              len(resp[0]) == 2 and isinstance(resp[0][1], dict)):
        resp = resp[0][1]  # [[201, {"k": "v"}]] to {"k": "v"}
      resp = resp.itervalues().next()  # {"obj": {"k": "v"}} to {"k": "v"}
      return dict(resp.items() + get_extra_items(resp).items())
    else:
      resp_code, resp_message = resp[0]
      raise exceptions.ContentDecodingError(
          messages.ExceptionsMessages.err_server_response.
          format(resp_code, resp_message))

  @staticmethod
  def set_obj_attrs(attrs, obj, **kwargs):
    """Update object according to new attributes exclude "type", "contact",
    "owners" due of objects assertion specific, and keyword arguments -
    attributes witch used to make JSON template to request and witch contain
    fully objects descriptions as dictionary.
    """
    obj.__dict__.update({k: v for k, v in attrs.iteritems()
                         if v and k not in ("type", "contact", "owners")})
    if kwargs:
      # for Audit objects
      if kwargs.get("program"):
        obj.program = kwargs["program"]
      # for Assessment, Assessment Template, Issues objects
      if kwargs.get("audit"):
        obj.audit = kwargs["audit"]
    return obj

  def create_objs(self, count, factory_params=None, **attrs_for_template):
    """Create new objects via REST API and return list of created objects with
    filtered attributes.
    """
    list_objs = self.create_list_objs(
        entity_factory=self.entities_factory_cls(), count=count,
        attrs_to_factory=factory_params, **attrs_for_template)
    return self.entities_factory_cls().filter_objs_attrs(
        objs=list_objs,
        attrs_to_include=self.entities_factory_cls().obj_attrs_names)

  def update_objs(self, objs, factory_params=None, **attrs_for_template):
    """Update existing objects via REST API and return list of updated objects
    with filtered attributes.
    """
    list_objs = self.update_list_objs(
        entity_factory=self.entities_factory_cls(),
        list_objs_to_update=string_utils.convert_to_list(objs),
        attrs_to_factory=factory_params, **attrs_for_template)
    return self.entities_factory_cls().filter_objs_attrs(
        objs=list_objs,
        attrs_to_include=self.entities_factory_cls().obj_attrs_names)

  def delete_objs(self, objs):
    """Delete existing objects via REST API."""
    return [self.client.delete_object(href=obj.href) for
            obj in string_utils.convert_to_list(objs)]


class HelpRestService(object):
  """Help class for interaction with business layer's services objects."""
  def __init__(self, endpoint):
    self.endpoint = endpoint
    self.client = RestClient(self.endpoint)


class ControlsService(BaseRestService):
  """Service for working with Controls entities."""
  def __init__(self):
    super(ControlsService, self).__init__(url.CONTROLS)


class ObjectivesService(BaseRestService):
  """Service for working with Objectives entities."""
  def __init__(self):
    super(ObjectivesService, self).__init__(url.OBJECTIVES)


class ProgramsService(BaseRestService):
  """Service for working with Programs entities."""
  def __init__(self):
    super(ProgramsService, self).__init__(url.PROGRAMS)


class AuditsService(BaseRestService):
  """Service for working with Audits entities."""
  def __init__(self):
    super(AuditsService, self).__init__(url.AUDITS)


class AssessmentTemplatesService(BaseRestService):
  """Service for working with Assessment Templates entities."""
  def __init__(self):
    super(AssessmentTemplatesService, self).__init__(url.ASSESSMENT_TEMPLATES)


class AssessmentsService(BaseRestService):
  """Service for working with Assessments entities."""
  def __init__(self):
    super(AssessmentsService, self).__init__(url.ASSESSMENTS)

  def create_objs(self, count, factory_params=None, **attrs_for_template):
    """Create new Assessments and make default relationships of Persons:
    'Creator', 'Assessor' to them via REST API and return list of created
    objects with filtered attributes.
    """
    objs = BaseRestService(url.ASSESSMENTS).create_objs(
        count, factory_params=None, **attrs_for_template)
    # add Default Person as 'Assessor', 'Creator' to Assessments
    RelationshipsService().map_objs(
        src_obj=ObjectPersonsFactory().default(), dest_objs=objs,
        attrs={"AssigneeType": "Creator,Assessor"})
    return objs


class IssuesService(BaseRestService):
  """Service for working with Issues entities."""
  def __init__(self):
    super(IssuesService, self).__init__(url.ISSUES)


class CustomAttributeDefinitionsService(BaseRestService):
  """Service for working with Custom Attributes entities."""
  def __init__(self):
    super(CustomAttributeDefinitionsService, self).__init__(
        url.CUSTOM_ATTRIBUTES)


class RelationshipsService(HelpRestService):
  """Service for creating relationships between entities."""
  def __init__(self):
    super(RelationshipsService, self).__init__(url.RELATIONSHIPS)

  def map_objs(self, src_obj, dest_objs, **attrs_for_template):
    """Create relationship from source to destination objects and
    return created.
    """
    return [self.client.create_object(
        type=objects.get_singular(self.endpoint), source=src_obj.__dict__,
        destination=dest_obj.__dict__, **attrs_for_template) for
        dest_obj in string_utils.convert_to_list(dest_objs)]


class ObjectsOwnersService(HelpRestService):
  """Service for assigning owners to entities."""
  def __init__(self):
    super(ObjectsOwnersService, self).__init__(url.OBJECT_OWNERS)

  def assign_owner_to_objs(self, objs, owner=ObjectPersonsFactory().default()):
    """Assign of an owner to objects."""
    return [self.client.create_object(
        type=objects.get_singular(self.endpoint), ownable=obj.__dict__,
        person=owner.__dict__) for obj in string_utils.convert_to_list(objs)]


class ObjectsInfoService(HelpRestService):
  """Service for getting information about entities."""
  def __init__(self):
    super(ObjectsInfoService, self).__init__(url.QUERY)

  def get_total_count_objs(self, obj_name):
    """Get and return total count of existing objects in system
    according to type of object.
    """
    resp = self.client.create_object(type=templates.COUNT,
                                     object_name=obj_name)
    dict_resp = json.loads(resp.text)[0]
    return dict_resp.get(obj_name).get("total")
