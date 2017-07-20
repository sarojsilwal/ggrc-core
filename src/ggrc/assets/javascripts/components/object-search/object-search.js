/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, $) {
  'use strict';

  GGRC.Components('objectSearch', {
    tag: 'object-search',
    template: can.view(GGRC.mustache_path +
      '/components/object-search/object-search.mustache'),
    viewModel: function () {
      return GGRC.VM.ObjectOperationsBaseVM.extend({
        isLoadingOrSaving: function () {
          return this.attr('is_loading');
        },
        object: 'MultitypeSearch',
        type: 'Program',
        availableTypes: function () {
          var types = GGRC.Mappings.getMappingTypes(
            this.attr('object'),
            ['TaskGroupTask', 'TaskGroup', 'CycleTaskGroupObjectTask'],
            []);
          return types;
        }
      });
    },
    events: {
      inserted: function () {
        this.setModel();
        this.viewModel.afterShown();
      },
      setModel: function () {
        var type = this.viewModel.attr('type');

        this.viewModel.attr('model', this.viewModel.modelFromType(type));
      },
      '{viewModel} type': function () {
        this.viewModel.attr('filter', '');
        this.viewModel.attr('afterSearch', false);
        this.viewModel.attr('relevant').replace([]);
        this.setModel();
        setTimeout(this.viewModel.onSubmit.bind(this.viewModel));
      }
    }
  });
})(window.can, window.can.$);
