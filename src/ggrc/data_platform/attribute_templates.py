# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Attribute templates module."""

from sqlalchemy import orm

from ggrc import db
from ggrc.data_platform import base


class AttributeTemplates(base.Base, db.Model):
  """Attribute templates model."""
  __tablename__ = 'attribute_templates'

  attribute_template_id = db.Column(db.Integer, primary_key=True)
  attribute_definition_id = db.Column(
      db.Integer,
      db.ForeignKey('attribute_definitions.attribute_definition_id')
  )
  object_template_id = db.Column(
      db.Integer,
      db.ForeignKey('object_templates.object_template_id')
  )
  namespace_id = db.Column(
      db.Integer, db.ForeignKey('namespaces.namespace_id'), nullable=True)
  order = db.Column(db.Integer)
  mandatory = db.Column(db.Boolean)
  unique = db.Column(db.Boolean)
  help_text = db.Column(db.UnicodeText)
  options = db.Column(db.UnicodeText)
  default_value = db.Column(db.UnicodeText)

  # ggrc specific code, needs to be added back to DP.
  read_only = db.Column(db.Boolean, default=False)

  attribute_definition = orm.relationship("AttributeDefinitions",
                                          backref="attribute_templates")
  object_template = orm.relationship("ObjectTemplates",
                                     backref="attribute_templates")
  namespace = orm.relationship("Namespaces", backref="attribute_templates")
