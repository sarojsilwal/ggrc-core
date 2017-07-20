# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Functions to remove references to obsolete entities from the DB."""

import sqlalchemy as sa


def _make_single_column_table(table_name, column_name, column_type=sa.String):
  """Creates a SQLAlchemy representation for a single column in a table."""
  return sa.sql.table(
      table_name,
      sa.sql.column(column_name, column_type),
  )


def replace(alembic_op, table_name, field, old_value, new_value):
  """UPDATE :table_name SET :field = :new_value WHERE :field = :old_value."""
  tbl = _make_single_column_table(table_name, field)
  alembic_op.execute(
      tbl.update().values({
          tbl.c[field]: new_value,
      }).where(
          tbl.c[field] == old_value,
      )
  )


def delete(alembic_op, table_name, field, value):
  """DELETE FROM :table WHERE :field = :value."""
  tbl = _make_single_column_table(table_name, field)
  alembic_op.execute(
      tbl.delete().where(
          tbl.c[field] == value,
      ),
  )
