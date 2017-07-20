# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Attribute definition module."""

from sqlalchemy import orm

from ggrc import db
from ggrc.data_platform import base


class AttributeDefinitions(base.Base, db.Model):
  """Attribute Definition model."""
  __tablename__ = 'attribute_definitions'

  attribute_definition_id = db.Column(db.Integer, primary_key=True)
  attribute_type_id = db.Column(
      db.Integer, db.ForeignKey('attribute_types.attribute_type_id'))
  name = db.Column(db.Unicode(length=255), nullable=False)
  display_name = db.Column(db.Unicode(length=255), nullable=False)
  namespace_id = db.Column(
      db.Integer, db.ForeignKey('namespaces.namespace_id'), nullable=True)

  attribute_type = orm.relationship(
      "AttributeTypes", backref="attribute_definitions")
  namespace = orm.relationship("Namespaces", backref="attribute_definitions")
