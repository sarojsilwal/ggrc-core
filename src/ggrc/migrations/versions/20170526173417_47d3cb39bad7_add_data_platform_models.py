# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
Add data platform models

Create Date: 2017-05-26 17:34:17.676564
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

import datetime

import sqlalchemy as sa
from sqlalchemy.sql import column
from sqlalchemy.sql import table

from alembic import op

# revision identifiers, used by Alembic.
revision = "47d3cb39bad7"
down_revision = "55575f96bb3c"


def create_tables():
  """Create tables for data platform models."""
  op.create_table(
      "namespaces",
      sa.Column("namespace_id", sa.Integer(), nullable=False),
      sa.Column("name", sa.Unicode(length=45), nullable=False),
      sa.Column("display_name", sa.Unicode(length=255), nullable=False),
      sa.Column("created_at", sa.DateTime(), nullable=False),
      sa.Column("updated_at", sa.DateTime(), nullable=False),
      sa.Column("updated_by_id", sa.Integer(), nullable=True),
      sa.Column("created_by_id", sa.Integer(), nullable=True),
      sa.ForeignKeyConstraint(["created_by_id"], ["people.id"], ),
      sa.ForeignKeyConstraint(["updated_by_id"], ["people.id"], ),
      sa.PrimaryKeyConstraint("namespace_id"),
      sa.UniqueConstraint("name")
  )
  op.create_table(
      "attribute_types",
      sa.Column("attribute_type_id", sa.Integer(), nullable=False),
      sa.Column("name", sa.Unicode(length=255), nullable=False),
      sa.Column("field_type", sa.Unicode(length=255), nullable=False),
      sa.Column("db_column_name", sa.Unicode(length=50), nullable=False),
      sa.Column("computed", sa.Boolean(), nullable=False, default=False),
      sa.Column("aggregate_function", sa.UnicodeText(), nullable=True),
      sa.Column("namespace_id", sa.Integer(), nullable=True),
      sa.Column("created_at", sa.DateTime(), nullable=False),
      sa.Column("updated_at", sa.DateTime(), nullable=False),
      # These two fields are nullable because we do not have front-end
      # interface for creating and modifying attribute types so they are all
      # created in migrations where users might not exist yet.
      sa.Column("updated_by_id", sa.Integer(), nullable=True),
      sa.Column("created_by_id", sa.Integer(), nullable=True),
      sa.ForeignKeyConstraint(["created_by_id"], ["people.id"], ),
      sa.ForeignKeyConstraint(["updated_by_id"], ["people.id"], ),
      sa.ForeignKeyConstraint(["namespace_id"], ["namespaces.namespace_id"], ),
      sa.PrimaryKeyConstraint("attribute_type_id")
  )
  op.create_table(
      "object_types",
      sa.Column("object_type_id", sa.Integer(), nullable=False),
      sa.Column("name", sa.Unicode(length=255), nullable=False),
      sa.Column("display_name", sa.Unicode(length=255), nullable=False),
      sa.Column("namespace_id", sa.Integer(), nullable=True),
      sa.Column("parent_object_type_id", sa.Integer(), nullable=True),
      sa.Column("created_at", sa.DateTime(), nullable=False),
      sa.Column("updated_at", sa.DateTime(), nullable=False),
      sa.Column("updated_by_id", sa.Integer(), nullable=True),
      sa.Column("created_by_id", sa.Integer(), nullable=True),
      sa.ForeignKeyConstraint(["created_by_id"], ["people.id"], ),
      sa.ForeignKeyConstraint(["updated_by_id"], ["people.id"], ),
      sa.ForeignKeyConstraint(["namespace_id"], ["namespaces.namespace_id"], ),
      sa.ForeignKeyConstraint(
          ["parent_object_type_id"],
          ["object_types.object_type_id"],
      ),
      sa.PrimaryKeyConstraint("object_type_id"),
      sa.UniqueConstraint("name", "namespace_id")
  )
  op.create_table(
      "attribute_definitions",
      sa.Column("attribute_definition_id", sa.Integer(), nullable=False),
      sa.Column("attribute_type_id", sa.Integer(), nullable=True),
      sa.Column("name", sa.Unicode(length=255), nullable=False),
      sa.Column("display_name", sa.Unicode(length=255), nullable=False),
      sa.Column("namespace_id", sa.Integer(), nullable=True),
      sa.Column("created_at", sa.DateTime(), nullable=False),
      sa.Column("updated_at", sa.DateTime(), nullable=False),
      sa.Column("updated_by_id", sa.Integer(), nullable=True),
      sa.Column("created_by_id", sa.Integer(), nullable=True),
      sa.ForeignKeyConstraint(
          ["attribute_type_id"],
          ["attribute_types.attribute_type_id"],
      ),
      sa.ForeignKeyConstraint(["created_by_id"], ["people.id"], ),
      sa.ForeignKeyConstraint(["updated_by_id"], ["people.id"], ),
      sa.ForeignKeyConstraint(["namespace_id"], ["namespaces.namespace_id"], ),
      sa.PrimaryKeyConstraint("attribute_definition_id")
  )
  op.create_table(
      "object_templates",
      sa.Column("object_template_id", sa.Integer(), nullable=False),
      sa.Column("object_type_id", sa.Integer(), nullable=True),
      sa.Column("name", sa.Unicode(length=255), nullable=False),
      sa.Column("display_name", sa.Unicode(length=255), nullable=False),
      sa.Column("namespace_id", sa.Integer(), nullable=True),
      sa.Column("created_at", sa.DateTime(), nullable=False),
      sa.Column("updated_at", sa.DateTime(), nullable=False),
      sa.Column("updated_by_id", sa.Integer(), nullable=True),
      sa.Column("created_by_id", sa.Integer(), nullable=True),
      sa.ForeignKeyConstraint(["created_by_id"], ["people.id"], ),
      sa.ForeignKeyConstraint(["updated_by_id"], ["people.id"], ),
      sa.ForeignKeyConstraint(["namespace_id"], ["namespaces.namespace_id"], ),
      sa.ForeignKeyConstraint(
          ["object_type_id"], ["object_types.object_type_id"], ),
      sa.PrimaryKeyConstraint("object_template_id")
  )
  op.create_table(
      "attribute_templates",
      sa.Column("attribute_template_id", sa.Integer(), nullable=False),
      sa.Column("attribute_definition_id", sa.Integer(), nullable=True),
      sa.Column("object_template_id", sa.Integer(), nullable=True),
      sa.Column("namespace_id", sa.Integer(), nullable=True),
      sa.Column("order", sa.Integer(), nullable=True),
      sa.Column("mandatory", sa.Boolean(), nullable=True),
      sa.Column("unique", sa.Boolean(), nullable=True),
      sa.Column("help_text", sa.UnicodeText(), nullable=True),
      sa.Column("options", sa.UnicodeText(), nullable=True),
      sa.Column("default_value", sa.UnicodeText(), nullable=True),
      sa.Column("read_only", sa.Boolean(), nullable=True),
      sa.Column("created_at", sa.DateTime(), nullable=False),
      sa.Column("updated_at", sa.DateTime(), nullable=False),
      sa.Column("updated_by_id", sa.Integer(), nullable=True),
      sa.Column("created_by_id", sa.Integer(), nullable=True),
      sa.ForeignKeyConstraint(
          ["attribute_definition_id"],
          ["attribute_definitions.attribute_definition_id"],
      ),
      sa.ForeignKeyConstraint(["created_by_id"], ["people.id"], ),
      sa.ForeignKeyConstraint(["updated_by_id"], ["people.id"], ),
      sa.ForeignKeyConstraint(["namespace_id"], ["namespaces.namespace_id"], ),
      sa.ForeignKeyConstraint(["object_template_id"], [
                              "object_templates.object_template_id"], ),
      sa.PrimaryKeyConstraint("attribute_template_id")
  )
  op.create_table(
      "attributes",
      sa.Column("attribute_id", sa.Integer(), nullable=False),
      sa.Column("object_id", sa.Integer(), nullable=True),
      sa.Column("object_type", sa.Unicode(length=250), nullable=True),
      sa.Column("attribute_definition_id", sa.Integer(), nullable=True),
      sa.Column("attribute_template_id", sa.Integer(), nullable=True),
      sa.Column("value_string", sa.UnicodeText(), nullable=True),
      sa.Column("value_integer", sa.Integer(), nullable=True),
      sa.Column("value_datetime", sa.DateTime(), nullable=True),
      sa.Column("source_type", sa.Unicode(length=250), nullable=True),
      sa.Column("source_id", sa.Integer(), nullable=True),
      sa.Column("source_attr", sa.Unicode(length=250), nullable=True),
      sa.Column("namespace_id", sa.Integer(), nullable=True),
      sa.Column("deleted", sa.Boolean(), nullable=True),
      sa.Column("version", sa.Integer(), nullable=True),
      sa.Column("created_at", sa.DateTime(), nullable=False),
      sa.Column("updated_at", sa.DateTime(), nullable=False),
      sa.Column("updated_by_id", sa.Integer(), nullable=True),
      sa.Column("created_by_id", sa.Integer(), nullable=True),
      sa.ForeignKeyConstraint(
          ["attribute_definition_id"],
          ["attribute_definitions.attribute_definition_id"],
      ),
      sa.ForeignKeyConstraint(
          ["attribute_template_id"],
          ["attribute_templates.attribute_template_id"],
      ),
      sa.ForeignKeyConstraint(["created_by_id"], ["people.id"], ),
      sa.ForeignKeyConstraint(["updated_by_id"], ["people.id"], ),
      sa.ForeignKeyConstraint(["namespace_id"], ["namespaces.namespace_id"], ),
      sa.PrimaryKeyConstraint("attribute_id")
  )
  op.create_index("ix_source", "attributes",
                  ["source_type", "source_id", "source_attr"], unique=False)
  op.create_index("ix_value_datetime", "attributes",
                  ["value_datetime"], unique=False)
  op.create_index("ix_value_integer", "attributes",
                  ["value_integer"], unique=False)


def populate_tables():
  """Create tables for data platform models."""
  # Due to old version of alembic we have to redefine the tables in order to
  # use them for insertion
  attribute_types = table(
      "attribute_types",
      column("attribute_type_id", sa.Integer),
      column("name", sa.Unicode),
      column("field_type", sa.Unicode),
      column("db_column_name", sa.Unicode),
      column("computed", sa.Boolean),
      column("aggregate_function", sa.UnicodeText),
      column("created_at", sa.DateTime),
      column("updated_at", sa.DateTime),
  )
  attribute_definitions = table(
      "attribute_definitions",
      column("attribute_definition_id", sa.Integer),
      column("attribute_type_id", sa.Integer),
      column("name", sa.Unicode),
      column("display_name", sa.Unicode),
      column("created_at", sa.DateTime),
      column("updated_at", sa.DateTime),
  )
  object_types = table(
      "object_types",
      column("object_type_id", sa.Integer),
      column("name", sa.Unicode),
      column("display_name", sa.Unicode),
      column("created_at", sa.DateTime),
      column("updated_at", sa.DateTime),
  )
  object_templates = table(
      "object_templates",
      column("object_template_id", sa.Integer),
      column("object_type_id", sa.Integer),
      column("name", sa.Unicode),
      column("display_name", sa.Unicode),
      column("created_at", sa.DateTime),
      column("updated_at", sa.DateTime),
  )
  attribute_templates = table(
      "attribute_templates",
      column("attribute_template_id", sa.Integer),
      column("attribute_definition_id", sa.Integer),
      column("object_template_id", sa.Integer),
      column("order", sa.Integer),
      column("read_only", sa.Boolean),
      column("created_at", sa.DateTime),
      column("updated_at", sa.DateTime),
  )

  op.bulk_insert(
      object_types,
      [{
          "object_type_id": 1,
          "name": u"basic_type",
          "display_name": u"Basic Object",
          "created_at": datetime.datetime.now(),
          "updated_at": datetime.datetime.now(),
      }]
  )
  op.bulk_insert(
      object_templates,
      [{
          "object_template_id": 1,
          "object_type_id": 1,
          "name": u"Control",
          "display_name": u"Control",
          "created_at": datetime.datetime.now(),
          "updated_at": datetime.datetime.now(),
      }, {
          "object_template_id": 2,
          "object_type_id": 1,
          "name": u"Objective",
          "display_name": u"Objective",
          "created_at": datetime.datetime.now(),
          "updated_at": datetime.datetime.now(),
      }]
  )
  op.bulk_insert(
      attribute_types,
      [{
          "attribute_type_id": 1,
          "name": u"Computed attribute for last assessment date",
          "field_type": u"computed_assessment_finished_date",
          "db_column_name": u"computed_assessment_finished_date",
          "computed": True,
          "aggregate_function": u"Assessment finished_date max",
          "created_at": datetime.datetime.now(),
          "updated_at": datetime.datetime.now(),
      }]
  )
  op.bulk_insert(
      attribute_definitions,
      [{
          "attribute_definition_id": 1,
          "attribute_type_id": 1,
          "name": u"last_assessment_date",
          "display_name": u"Last Assessment Date",
          "created_at": datetime.datetime.now(),
          "updated_at": datetime.datetime.now(),
      }]
  )
  op.bulk_insert(
      attribute_templates,
      [{
          "attribute_template_id": 1,
          "attribute_definition_id": 1,
          "object_template_id": 1,
          "order": 1,
          "read_only": True,
          "created_at": datetime.datetime.now(),
          "updated_at": datetime.datetime.now(),
      }, {
          "attribute_template_id": 2,
          "attribute_definition_id": 1,
          "object_template_id": 2,
          "order": 1,
          "read_only": True,
          "created_at": datetime.datetime.now(),
          "updated_at": datetime.datetime.now(),
      }]
  )


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  create_tables()
  populate_tables()


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  op.drop_index("ix_value_integer", table_name="attributes")
  op.drop_index("ix_value_datetime", table_name="attributes")
  op.drop_index("ix_source", table_name="attributes")
  op.drop_table("attributes")
  op.drop_table("attribute_templates")
  op.drop_table("object_templates")
  op.drop_table("attribute_definitions")
  op.drop_table("object_types")
  op.drop_table("attribute_types")
  op.drop_table("namespaces")
