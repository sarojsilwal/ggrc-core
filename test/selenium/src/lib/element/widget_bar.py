# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Widget bar elements."""

import re

from lib import base, factory
from lib.constants import element, regex
from lib.utils import selenium_utils


class Tab(base.Tab):
  "Tab base elements."
  # pylint: disable=too-few-public-methods
  def __init__(self, driver, _locator_or_element):
    """
    Args: driver (base.CustomDriver
    """
    super(Tab, self).__init__(driver, _locator_or_element)
    self.member_count = None
    self._set_member_count()

  def _set_member_count(self):
    "Select member count."
    widget_title = selenium_utils.get_when_visible(
        self._driver, self.locator_or_element).text
    if "(" not in widget_title:
      self.member_count = int(widget_title)
    else:
      self.member_count = int(
          re.match(regex.WIDGET_TITLE_AND_COUNT, widget_title).group(2))


class AddWidget(base.Component):
  """Model for add widget button in Widget bar. No elements are initiated
 here because based on context they may be missing.
 """

  def _select(self, widget_name):
    """Selects widget from Dropdown and return appropriate
    initialized Widget class"""
    self._driver.find_element(
        *factory.get_locator_add_widget(widget_name)).click()
    return factory.get_cls_widget(widget_name)(self._driver)

  def select_controls(self):
    """
    Return: lib.page.widget.generic_widget.Controls
    """
    return self._select(element.WidgetBar.CONTROLS)

  def select_issues(self):
    """
    Return: lib.page.widget.generic_widget.Issues
    """
    return self._select(element.WidgetBar.ISSUES)

  def select_processes(self):
    """
    Return: lib.page.widget.generic_widget.Processes
    """
    return self._select(element.WidgetBar.PROCESSES)

  def select_data_assets(self):
    """
    Return: lib.page.widget.generic_widget.DataAssets
    """
    return self._select(element.WidgetBar.DATA_ASSETS)

  def select_systems(self):
    """
    Return: lib.page.widget.generic_widget.Systems
    """
    return self._select(element.WidgetBar.SYSTEMS)

  def select_products(self):
    """
    Return: lib.page.widget.generic_widget.Products
    """
    return self._select(element.WidgetBar.PRODUCTS)

  def select_projects(self):
    """
    Return: lib.page.widget.generic_widget.Projects
    """
    return self._select(element.WidgetBar.PROJECTS)

  def select_programs(self):
    """
    Return: lib.page.widget.generic_widget.Programs
    """
    return self._select(element.WidgetBar.PROGRAMS)
