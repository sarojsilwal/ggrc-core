/*!
    Copyright (C) 2017 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

(function (can, GGRC) {
  'use strict';

  GGRC.Components('effective-dates', {
    tag: 'effective-dates',
    template: can.view(
      GGRC.mustache_path +
      '/components/effective-dates/effective-dates.mustache'
    ),
    scope: {
      instance: null,
      configStartDate: {
        label: 'Effective Date',
        helpText: 'Enter the date this object becomes effective.',
        required: false
      },
      configEndDate: {
        label: 'Last Deprecated Date',
        helpText: 'Enter the date this object stops being effective.',
        required: false
      }
    }
  });
})(window.can, window.GGRC);
