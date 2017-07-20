# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Issue Model."""

from ggrc import db
from ggrc.access_control.roleable import Roleable
from ggrc.models.deferred import deferred
from ggrc.models.mixins import (
    BusinessObject, LastDeprecatedTimeboxed, CustomAttributable, TestPlanned
)
from ggrc.models.mixins.audit_relationship import AuditRelationship
from ggrc.models.object_document import PublicDocumentable
from ggrc.models.object_owner import Ownable
from ggrc.models.object_person import Personable
from ggrc.models.relationship import Relatable
from ggrc.models.track_object_state import HasObjectState
from ggrc.fulltext.mixin import Indexed


class Issue(Roleable, HasObjectState, TestPlanned, CustomAttributable,
            PublicDocumentable, Personable, LastDeprecatedTimeboxed, Ownable,
            Relatable, AuditRelationship, BusinessObject, Indexed, db.Model):
  """Issue Model."""

  __tablename__ = 'issues'

  VALID_STATES = [
      "Draft",
      "Active",
      "Deprecated",
      "Fixed",
      "Fixed and Verified"
  ]

  # REST properties
  _publish_attrs = [
      "audit"
  ]

  _aliases = {
      "url": "Issue URL",
      "test_plan": {
          "display_name": "Remediation Plan"
      },
      "status": {
          "display_name": "State",
          "mandatory": False,
          "description": "Options are: \n{} ".format('\n'.join(VALID_STATES))
      },
  }

  audit_id = deferred(
      db.Column(db.Integer, db.ForeignKey('audits.id'), nullable=False),
      'Issue')
