# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

from ggrc import db
from ggrc.access_control.roleable import Roleable
from ggrc.fulltext.mixin import Indexed
from ggrc.models.mixins import (CustomAttributable, BusinessObject,
                                LastDeprecatedTimeboxed)
from ggrc.models.object_person import Personable
from ggrc.models.object_owner import Ownable
from ggrc.models.relationship import Relatable
from ggrc.models.track_object_state import HasObjectState


class Threat(Roleable, HasObjectState, CustomAttributable, Personable,
             Relatable, LastDeprecatedTimeboxed, Ownable, BusinessObject,
             Indexed, db.Model):
  __tablename__ = 'threats'

  _aliases = {
      "url": "Threat URL",
  }
