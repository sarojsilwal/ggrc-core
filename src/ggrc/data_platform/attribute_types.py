# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Attribute types module."""

from sqlalchemy import orm

from ggrc import db
from ggrc.data_platform import base


class AttributeTypes(base.Base, db.Model):
  """Attribute types model."""
  __tablename__ = 'attribute_types'

  attribute_type_id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.Unicode(length=255), nullable=False)
  field_type = db.Column(db.Unicode(length=255), nullable=False)
  db_column_name = db.Column(db.Unicode(length=50), nullable=False)
  computed = db.Column(db.Boolean, nullable=False, default=False)
  aggregate_function = db.Column(db.UnicodeText())

  namespace_id = db.Column(
      db.Integer, db.ForeignKey('namespaces.namespace_id'), nullable=True)

  namespace = orm.relationship("Namespaces", backref="attribute_types")
