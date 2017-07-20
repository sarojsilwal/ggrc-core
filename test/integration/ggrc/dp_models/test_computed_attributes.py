# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>

"""Test last assessment module."""


from ggrc.data_platform import computed_attributes

from integration.ggrc import TestCase


class TestComputedAttributes(TestCase):
  """Integration test suite for computed attributes module."""

  def test_get_computed_attributes(self):
    attributes = computed_attributes.get_computed_attributes()
    attribute_names = {
        (attr.object_template.name, attr.attribute_definition.name)
        for attr in attributes
    }
    self.assertEqual(
        attribute_names,
        {
            ("Control", "last_assessment_date"),
            ("Objective", "last_assessment_date"),
        }
    )
