# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Object types module."""

from sqlalchemy import orm
from sqlalchemy.ext.declarative import declared_attr

from ggrc import db
from ggrc.data_platform import base


class ObjectTypes(base.Base, db.Model):
  """Object types model."""
  __tablename__ = 'object_types'

  object_type_id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.Unicode(length=255), nullable=False)
  display_name = db.Column(db.Unicode(length=255),
                           nullable=False)

  namespace_id = db.Column(
      db.Integer, db.ForeignKey('namespaces.namespace_id'), nullable=True)
  parent_object_type_id = db.Column(
      db.Integer,
      db.ForeignKey('object_types.object_type_id')
  )

  namespace = orm.relationship("Namespaces", backref="object_types")
  parent_object_type = orm.relationship(
      "ObjectTypes",
      backref="child_object_types",
      remote_side='ObjectTypes.object_type_id'
  )

  @declared_attr
  def __table_args__(cls):  # pylint: disable=no-self-argument
    return (
        db.UniqueConstraint("name", "namespace_id"),
    )
