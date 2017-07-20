/*!
    Copyright (C) 2017 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

(function (can) {
  'use strict';

  var template = can.view(GGRC.mustache_path +
    '/components/assessment/info-pane/inline-item.mustache');

  GGRC.Components('assessmentInlineItem', {
    tag: 'assessment-inline-item',
    template: template,
    viewModel: {
      instance: {},
      propName: '@',
      value: '',
      type: '@',
      dropdownOptions: [],
      dropdownClass: '@',
      dropdownNoValue: false,
      withReadMore: false,
      isEditIconDenied: false,
      onStateChangeDfd: can.Deferred().resolve()
    }
  });
})(window.can);
