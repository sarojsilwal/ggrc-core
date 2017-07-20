# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Remove Request relationships."""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

from alembic import op

from ggrc.migrations.utils.cleanup import delete


# revision identifiers, used by Alembic.
revision = '59aaa4750320'
down_revision = '55501ef0f634'


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  delete(op, "task_group_objects", "object_type", value="Request")


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  # nothing to do
  pass
