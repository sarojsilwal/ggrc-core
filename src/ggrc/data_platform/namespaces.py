# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Namespaces module."""

from ggrc import db
from ggrc.data_platform import base


class Namespaces(base.Base, db.Model):
  """Namespaces model."""
  __tablename__ = 'namespaces'

  namespace_id = db.Column(
      db.Integer, primary_key=True
  )
  name = db.Column(db.Unicode(length=45), nullable=False, unique=True)
  display_name = db.Column(db.Unicode(length=255), nullable=False)
