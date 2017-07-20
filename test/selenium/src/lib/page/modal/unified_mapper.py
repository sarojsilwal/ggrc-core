# Copyright (C) 2017 Google Inc.
# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""Modals for map objects."""

from lib import base
from lib.constants import locator
from lib.utils import filter_utils, selenium_utils


class CommonUnifiedMapperModal(base.Modal):
  """Common unified mapper modal."""
  _locators = locator.ModalMapObjects

  def __init__(self, driver, obj_name):
    super(CommonUnifiedMapperModal, self).__init__(driver)
    # labels
    self.title_modal = base.Label(driver, self._locators.MODAL_TITLE)
    self.obj_type = base.Label(driver, self._locators.OBJ_TYPE)
    self.filter_by_expression = base.Label(
        driver, self._locators.FILTER_BY_EXPRESSION)
    # user input elements
    self.filter_via_expression_text_box = base.TextInputField(
        driver, self._locators.FILTER_VIA_EXPRESSION_TEXT_BOX)
    self.filter_by_state_text_box = base.DropdownStatic(
        driver, self._locators.FILTER_BY_STATE_DROPDOWN,
        self._locators.FILTER_BY_STATE_DROPDOWN_OPTIONS)
    self.tree_view = base.UnifiedMapperTreeView(driver, obj_name=obj_name)

  def _select_dest_obj_type(self, obj_name, is_asmts_generation=False):
    """Open dropdown and select element according to destination object name.
    If is_asmts_generation then TextFilterDropdown, else DropdownStatic.
    """
    if obj_name:
      obj_type_dropdown = base.DropdownStatic(
          self._driver, self._locators.OBJ_TYPE_DROPDOWN,
          self._locators.OBJ_TYPE_DROPDOWN_OPTIONS)
      obj_type_dropdown.select(obj_name)
      if is_asmts_generation:
        asmt_tmpl_dropdown = base.TextFilterDropdown(
            self._driver, self._locators.OBJ_TYPE_DROPDOWN,
            self._locators.OBJ_TYPE_DROPDOWN_OPTIONS)
        asmt_tmpl_dropdown.find_and_select_el_by_text(obj_name)

  def _filter_dest_objs_via_expression_by_titles(self, objs_titles):
    """Enter expression is like 'title=obj1_title or title=obj2_title' into
    filter via expression text box according to destination objects titles.
    """
    # pylint: disable=invalid-name
    expression = filter_utils.FilterUtils.get_filter_exp_by_title(
        titles=objs_titles)
    self.filter_via_expression_text_box.enter_text(expression)

  def _select_search_dest_objs(self):
    """Click Search button to search objects according set filters."""
    base.Button(self._driver, self._locators.BUTTON_SEARCH).click()

  def _select_dest_objs_to_map(self, objs_titles):
    """Select checkboxes regarding to titles from list of checkboxes
    according to destinations objects titles.
    """
    dest_objs = base.ListCheckboxes(
        self._driver, self._locators.FOUND_OBJECTS_TITLES,
        self._locators.FOUND_OBJECTS_CHECKBOXES)
    dest_objs.select_by_titles(objs_titles)

  def get_mapping_statuses(self):
    """Get mapping status from checkboxes on Unified Mapper
       (selected and disabled or not).
    """
    dest_objs = base.ListCheckboxes(
        self._driver, self._locators.FOUND_OBJECTS_TITLES,
        self._locators.FOUND_OBJECTS_CHECKBOXES)
    return (
        dest_objs.get_mapping_statuses() if
        self.tree_view.tree_view_items() else [])

  def _confirm_map_selected(self):
    """Select Map Selected button to confirm map selected objects to
    source object.
    """
    base.Button(self._driver, self._locators.BUTTON_MAP_SELECTED).click()
    selenium_utils.get_when_invisible(
        self._driver, self._locators.BUTTON_MAP_SELECTED)
    selenium_utils.get_when_invisible(
        self._driver, locator.TreeView.NO_RESULTS_MESSAGE)

  def search_dest_objs(self, dest_objs_type, dest_objs_titles,
                       is_asmts_generation=False):
    """Filter and search destination objects according to them type and titles.
    If is_asmts_generation then TextFilterDropdown is using.
    """
    self._select_dest_obj_type(obj_name=dest_objs_type,
                               is_asmts_generation=is_asmts_generation)
    self._filter_dest_objs_via_expression_by_titles(
        objs_titles=dest_objs_titles)
    self._select_search_dest_objs()
    return self.tree_view.get_list_members_as_list_scopes()

  def map_dest_objs(self, dest_objs_type, dest_objs_titles,
                    is_asmts_generation=False):
    """Filter, search destination objects according to them type and titles.
    Map found destination objects to source object.
    If is_asmts_generation then TextFilterDropdown is using.
    """
    self.search_dest_objs(dest_objs_type, dest_objs_titles,
                          is_asmts_generation=is_asmts_generation)
    self._select_dest_objs_to_map(objs_titles=dest_objs_titles)
    self._confirm_map_selected()


class MapObjectsModal(CommonUnifiedMapperModal):
  """Modal for map objects."""
  _locators = locator.ModalMapObjects

  def __init__(self, driver, obj_name):
    super(MapObjectsModal, self).__init__(driver, obj_name)


class SearchObjectsModal(CommonUnifiedMapperModal):
  """Modal for search objects."""
  _locators = locator.ModalMapObjects

  def __init__(self, driver, obj_name):
    super(SearchObjectsModal, self).__init__(driver, obj_name)


class GenerateAssessmentsModal(CommonUnifiedMapperModal):
  """Modal for map objects."""
  _locators = locator.ModalGenerateAssessments

  def generate_asmts(self, objs_under_asmt_titles, asmt_tmpl_title=None):
    """Filter, search objects under Assessment according to them titles:
    objects under assessments titles, if 'asmt_tmpl_title'
    then Assessment Template title.
    Generate Assessments based on found objects under Assessment.
    """
    # pylint: disable=invalid-name
    self.map_dest_objs(
        dest_objs_type=asmt_tmpl_title,
        dest_objs_titles=objs_under_asmt_titles, is_asmts_generation=True)
