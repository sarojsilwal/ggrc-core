# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Module containing custom attributable mixin."""

from logging import getLogger

from sqlalchemy import and_
from sqlalchemy import orm
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import foreign
from sqlalchemy.orm import relationship

from ggrc import builder


# pylint: disable=invalid-name
logger = getLogger(__name__)


# pylint: disable=attribute-defined-outside-init; CustomAttributable is a mixin
class Attributable(object):
  """Custom Attributable mixin."""

  _publish_attrs = [
      'attributes',
  ]
  _update_attrs = []

  @declared_attr
  def _attributes(cls):  # pylint: disable=no-self-argument
    """Load custom attribute definitions"""
    from ggrc.models.all_models import Attributes

    def join_function():
      """Object and CAD join function."""
      object_id = foreign(Attributes.object_id)
      object_type = foreign(Attributes.object_type)
      return and_(object_id == cls.id, object_type == unicode(cls.__name__))

    return relationship(
        "Attributes",
        primaryjoin=join_function,
        viewonly=True,
    )

  @builder.simple_property
  def attributes(self):
    return {
        attr.attribute_template.attribute_definition.name: {
            "value": attr.value_datetime
        }
        for attr in self._attributes  # pylint: disable=not-an-iterable
    }

  @classmethod
  def eager_query(cls):
    """Define fields to be loaded eagerly to lower the count of DB queries."""
    query = super(Attributable, cls).eager_query()
    query = query.options(
        orm.subqueryload('_attributes')
    )
    return query
