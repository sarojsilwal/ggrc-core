# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Base module."""

from sqlalchemy.ext.declarative import declared_attr

from ggrc import db
from ggrc.models.inflector import ModelInflectorDescriptor


class Base(object):
  """Base Model for data platform models."""
  created_at = db.Column(db.DateTime, nullable=False)
  updated_at = db.Column(db.DateTime, nullable=False)

  # Note for created_by_id and updated_by_id
  # This field is nullable because we do not have front-end interface for
  # creating and modifying attributes type entries
  @declared_attr
  def created_by_id(cls):  # pylint: disable=no-self-argument
    return db.Column(db.Integer, db.ForeignKey('people.id'), nullable=True)

  @declared_attr
  def updated_by_id(cls):  # pylint: disable=no-self-argument
    """Id of user who did the last modification of the object."""
    return db.Column(db.Integer, db.ForeignKey('people.id'), nullable=True)

  @declared_attr
  def modified_by(cls):  # pylint: disable=no-self-argument
    """Relationship to user referenced by updated_by_id."""
    return db.relationship(
        'Person',
        primaryjoin='{}.updated_by_id == Person.id'.format(cls.__name__),
        foreign_keys='{}.updated_by_id'.format(cls.__name__),
        uselist=False,
    )

  @declared_attr
  def created_by(cls):  # pylint: disable=no-self-argument
    """Relationship to user referenced by updated_by_id."""
    return db.relationship(
        'Person',
        primaryjoin='{}.created_by_id == Person.id'.format(cls.__name__),
        foreign_keys='{}.created_by_id'.format(cls.__name__),
        uselist=False,
    )

  _inflector = ModelInflectorDescriptor()
