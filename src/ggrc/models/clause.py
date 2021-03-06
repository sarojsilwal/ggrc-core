# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Module for Clause model."""
from sqlalchemy import orm

from ggrc import db
from ggrc.access_control.roleable import Roleable
from ggrc.models.mixins import CustomAttributable
from ggrc.models.deferred import deferred
from ggrc.models.mixins import Hierarchical
from ggrc.models.mixins import LastDeprecatedTimeboxed
from ggrc.models.mixins import BusinessObject
from ggrc.models.object_owner import Ownable
from ggrc.models.object_person import Personable
from ggrc.models.relationship import Relatable
from ggrc.models.track_object_state import HasObjectState
from ggrc.fulltext.mixin import Indexed


class Clause(Roleable, HasObjectState, Hierarchical, CustomAttributable,
             Personable, Ownable, LastDeprecatedTimeboxed, Relatable,
             BusinessObject, Indexed, db.Model):

  __tablename__ = 'clauses'
  _table_plural = 'clauses'
  _aliases = {
      "url": "Clause URL",
      "description": "Text of Clause",
      "directive": None,
  }

  # pylint: disable=invalid-name
  na = deferred(db.Column(db.Boolean, default=False, nullable=False),
                'Clause')
  notes = deferred(db.Column(db.Text), 'Clause')

  _publish_attrs = [
      'na',
      'notes',
  ]
  _fulltext_attrs = [
      'na',
      'notes',
  ]

  @classmethod
  def indexed_query(cls):
    query = super(Clause, cls).indexed_query()
    return query.options(
        orm.Load(cls).load_only(
            "na",
            "notes",
        )
    )

  _sanitize_html = ['notes']
  _include_links = []
