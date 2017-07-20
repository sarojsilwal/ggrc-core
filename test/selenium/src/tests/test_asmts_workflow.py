# Copyright (C) 2017 Google Inc., authors, and contributors <see AUTHORS file>
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Assessments Workflow smoke tests."""
# pylint: disable=no-self-use
# pylint: disable=invalid-name
# pylint: disable=unused-argument
# pylint: disable=too-few-public-methods

import pytest

from lib import base
from lib.constants import messages
from lib.entities import entities_factory
from lib.service import webui_service


class TestAssessmentsWorkflow(base.Test):
  """Tests for Assessments Workflow functionality."""

  @pytest.mark.smoke_tests
  def test_add_comment_to_asmt_via_info_panel(
      self, new_program_rest, new_audit_rest, new_assessment_rest, selenium
  ):
    """Check via UI of possibility to correctly add comment to Assessment via
    Info Panel.
    Preconditions:
    - Program created via REST API.
    - Audit created under Program via REST API.
    - Assessment created under Audit via REST API.
    Test parameters: None
    """
    expected_asmt = new_assessment_rest
    expected_asmt_comments = [entities_factory.CommentsFactory().
                              create().repr_ui()]
    # due to 'actual_asmt.updated_at = None'
    (expected_asmt.
     update_attrs(comments=expected_asmt_comments, updated_at=None).repr_ui())
    assessments_service = webui_service.AssessmentsService(selenium)
    asmt_comments_panel = assessments_service.add_comments(
        src_obj=new_audit_rest, obj=expected_asmt,
        comment_objs=expected_asmt_comments)
    assert asmt_comments_panel.is_input_empty is True
    actual_asmt = (
        webui_service.AssessmentsService(selenium).
        get_list_objs_from_info_panels(
            src_obj=new_audit_rest, objs=expected_asmt).update_attrs(
            comments={"created_at": None}, is_replace_dicts_values=True))
    assert expected_asmt == actual_asmt, (
        messages.AssertionMessages.
        format_err_msg_equal(expected_asmt, actual_asmt))
