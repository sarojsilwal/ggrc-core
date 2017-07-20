# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Tests for Issue model."""
from ggrc.models import all_models
from integration.ggrc import TestCase, Api
from integration.ggrc.models import factories


class TestIssue(TestCase):
  """ Test Issue class. """
  def setUp(self):
    super(TestIssue, self).setUp()
    self.api = Api()
    with factories.single_commit():
      audit = factories.AuditFactory()
      for status in all_models.Issue.VALID_STATES:
        factories.IssueFactory(audit=audit, status=status)

  def test_filter_by_status(self):
    """Test Issue filtering by status."""
    query_request_data = [{
        'fields': [],
        'filters': {
            'expression': {
                'left': {
                    'left': 'status',
                    'op': {'name': '='},
                    'right': 'Fixed'
                },
                'op': {'name': 'OR'},
                'right': {
                    'left': 'status',
                    'op': {'name': '='},
                    'right': 'Fixed and Verified'
                },
            },
        },
        'object_name': 'Issue',
        'permissions': 'read',
        'type': 'values',
    }]
    response = self.api.send_request(
        self.api.client.post,
        data=query_request_data,
        api_link="/query"
    )
    self.assertEqual(response.status_code, 200)

    statuses = {i["status"] for i in response.json[0]["Issue"]["values"]}
    self.assertEqual(statuses, {"Fixed", "Fixed and Verified"})
