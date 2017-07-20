# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Integration tests for WithLastAssessmentDate logic.

Test cases:

 - Last assessment date on Parent Control
 - Last assessment date on Control Snapshot
 - Index Entries for Parent Controls
 - Index Entries for Snapshots

Changes that trigger updates of dates:

 - Snapshot created (should get date from the original object)
 - Snapshot mapped to assessment
 - Assessment deleted
 - Assessment finished
 - Assessment moved from finished state to any other

Corner cases:

 - Updating dates on snapshots when the original object does not exist

"""

import datetime

import freezegun

from ggrc import models
from integration.ggrc import TestCase
from integration.ggrc.api_helper import Api
from integration.ggrc.models import factories


class TestLastAssessmentDate(TestCase):
  """Integration test suite for WithLastAssessmentDate functionality.

  Setup stage for these tests consists of:
    - 5 controls (Control_0, Control_1, Control_2, Control_3, Control_4)
    - 2 Objectives (Objective_0, Objective_1)
    - 2 audits
      - Audit_0 with snapshots of
        - Control_0, Control_1, Objective_0
      - Audit_1 with snapshots of
        -Control_1, Control_2, Control_3, Objective_0, Objective_1
    - 2 Assessments
      - Assessment_0 on Audit_0 with snapshot mappings for
        - Control_1, Objective_0
      - Assessment_1 on Audit_1 with snapshot mappings for
        - Control_1, Control_2, Objective_0, Objective_1
  """

  def setUp(self):
    super(TestLastAssessmentDate, self).setUp()
    self.api = Api()
    self.client.get("/login")
    person = models.Person.query.first()
    with factories.single_commit():
      controls = [
          factories.ControlFactory(title="Control_{}".format(i),
                                   owners=[person])
          for i in range(5)
      ]
      objectives = [
          factories.ObjectiveFactory(title="Objective_{}".format(i),
                                     owners=[person])
          for i in range(2)
      ]
      audit_0 = factories.AuditFactory(title="Audit_0", contact=person)
      audit_1 = factories.AuditFactory(title="Audit_1", contact=person)
      audit_0_snapshots = self._create_snapshots(
          audit_0, controls[:2] + objectives[:1])
      audit_1_snapshots = self._create_snapshots(
          audit_1, controls[1:4] + objectives)
      assessment_0 = factories.AssessmentFactory(
          title="Assessment_0", audit=audit_0)
      assessment_1 = factories.AssessmentFactory(
          title="Assessment_1", audit=audit_1)
      factories.RelationshipFactory(source=assessment_0, destination=audit_0)
      factories.RelationshipFactory(source=audit_1, destination=assessment_1)

      # Audit 0 assessment mappings:
      factories.RelationshipFactory(
          source=assessment_0,
          destination=audit_0_snapshots[1],  # snapshot of control_1
      )
      factories.RelationshipFactory(
          source=assessment_0,
          destination=audit_0_snapshots[2],  # snapshot of objective_0
      )
      # Audit 1 assessment mappings:
      factories.RelationshipFactory(
          source=audit_1_snapshots[0],  # snapshot of control_1
          destination=assessment_1,
      )
      factories.RelationshipFactory(
          source=assessment_1,
          destination=audit_1_snapshots[1],  # snapshot of control_2
      )
      factories.RelationshipFactory(
          source=assessment_1,
          destination=audit_1_snapshots[3],  # snapshot of objective_0
      )
      factories.RelationshipFactory(
          source=audit_1_snapshots[4],  # snapshot of objective_1
          destination=assessment_1,
      )

  def test_no_finished_assessment(self):
    """Test empty last assessment dates."""
    controls = models.Control.query.all()
    for control in controls:
      self.assertEqual(control.last_assessment_date, None)

    snapshots = models.Snapshot.query.all()
    for snapshot in snapshots:
      self.assertEqual(snapshot.last_assessment_date, None)

  def test_single_finished_assessment(self):
    finish_date = datetime.datetime(2017, 2, 20, 13, 40, 0)
    related_objects = {"Control_1", "Objective_0"}

    with freezegun.freeze_time(finish_date):
      asmt = models.Assessment.query.filter_by(title="Assessment_0").first()
      self.api.put(asmt, {"status": "Completed"})

    for control in models.Control.query.all():
      if control.title in related_objects:
        self.assertEqual(control.last_assessment_date, finish_date)
      else:
        self.assertEqual(control.last_assessment_date, None)

    for snapshot in models.Snapshot.query.all():
      if snapshot.revision.content["title"] in related_objects:
        self.assertEqual(snapshot.last_assessment_date, finish_date)
      else:
        self.assertEqual(snapshot.last_assessment_date, None)
