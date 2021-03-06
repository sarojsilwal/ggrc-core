# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

from ggrc import db
from ggrc.access_control.roleable import Roleable
from ggrc.fulltext.mixin import Indexed
from .mixins import (BusinessObject, LastDeprecatedTimeboxed,
                     CustomAttributable)
from .object_person import Personable
from .object_owner import Ownable
from .relationship import Relatable
from .track_object_state import HasObjectState


class Market(Roleable, HasObjectState, CustomAttributable, Personable,
             Relatable, LastDeprecatedTimeboxed, Ownable,
             BusinessObject, Indexed, db.Model):
  __tablename__ = 'markets'
  _aliases = {"url": "Market URL"}
