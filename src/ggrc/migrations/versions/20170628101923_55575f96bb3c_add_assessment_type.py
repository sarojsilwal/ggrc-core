# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""
Add assessment_type field to Assessment

Create Date: 2017-06-28 10:19:23.789991
"""
# disable Invalid constant name pylint warning for mandatory Alembic variables.
# pylint: disable=invalid-name

import sqlalchemy as sa

from alembic import op


# revision identifiers, used by Alembic.
revision = '55575f96bb3c'
down_revision = '436dc4cea0f3'


def upgrade():
  """Upgrade database schema and/or data, creating a new revision."""
  op.add_column(
      'assessments',
      sa.Column(
          'assessment_type',
          sa.String(length=250),
          nullable=False,
          server_default="Control",
      )
  )
  # Change CA help text "Assessment type" to "Assessment Category"
  op.execute(
      'UPDATE custom_attribute_definitions '
      'SET helptext = "Assessment Category" '
      'WHERE helptext = "Assessment type" '
      'AND definition_type = "assessment" AND title = "Type";'
  )


def downgrade():
  """Downgrade database schema and/or data back to the previous revision."""
  op.drop_column('assessments', 'assessment_type')
  op.execute(
      'UPDATE custom_attribute_definitions '
      'SET helptext = "Assessment type" '
      'WHERE helptext = "Assessment Category"'
      'AND definition_type = "assessment" AND title = "Type";'
  )
