# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

from flask.ext.sqlalchemy import SQLAlchemy


def get_db():
  """Get modified db object."""
  db = SQLAlchemy()

  class String(db.String):
    """Simple subclass of sqlalchemy.orm.String which provides a default
    length for `String` types to satisfy MySQL
    """

    def __init__(self, length=None, *args, **kwargs):
      # TODO: Check for MySQL and only apply when needed
      if length is None:
        length = 250
      return super(String, self).__init__(length, *args, **kwargs)
  db.String = String
  return db
