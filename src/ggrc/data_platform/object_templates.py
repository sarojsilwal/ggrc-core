# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Object templates module."""

from sqlalchemy import orm

from ggrc import db
from ggrc.data_platform import base


class ObjectTemplates(base.Base, db.Model):
  """Object Templates model."""
  __tablename__ = 'object_templates'

  object_template_id = db.Column(db.Integer, primary_key=True)
  object_type_id = db.Column(
      db.Integer,
      db.ForeignKey('object_types.object_type_id')
  )
  name = db.Column(db.Unicode(length=255), nullable=False)
  display_name = db.Column(db.Unicode(length=255), nullable=False)

  namespace_id = db.Column(
      db.Integer, db.ForeignKey('namespaces.namespace_id'), nullable=True)

  object_type = orm.relationship("ObjectTypes", backref="object_templates")

  namespace = orm.relationship("Namespaces", backref="object_templates")
