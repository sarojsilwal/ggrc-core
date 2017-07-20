/*!
 Copyright (C) 2017 Google Inc., authors, and contributors
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */
(function (can, GGRC, CMS) {
  'use strict';

  GGRC.Components('mapperToolbar', {
    tag: 'mapper-toolbar',
    template: can.view(
      GGRC.mustache_path +
      '/components/unified-mapper/mapper-toolbar.mustache'
    ),
    viewModel: {
      filter: '',
      statusFilter: '',
      dropdown_options: [],
      statuses: [],
      isLoading: false,
      totalObjects: 0,
      objectsPlural: false,
      showStatusFilter: false,
      displayPrefs: null,
      type: '',
      afterSearch: false,
      init: function () {
        var self = this;
        CMS.Models.DisplayPrefs.getSingleton().then(function (displayPrefs) {
          self.attr('displayPrefs', displayPrefs);
          setTimeout(self.setStatusFilter.bind(self));
        });
      },
      onSubmit: function () {
        this.dispatch('submit');
        if (this.attr('showStatusFilter')) {
          this.saveStatusFilter();
        }
      },
      onReset: function () {
        this.attr('filter', '');
        this.attr('statuses', []);
        this.attr('statusFilter', '');
        this.dispatch('submit');
      },
      getModelName: function () {
        var Model = CMS.Models[this.attr('type')];
        return Model.model_singular;
      },
      setStatusFilter: function () {
        var modelName = this.getModelName();
        var showStatusFilter = GGRC.Utils.State.hasState(modelName);
        var dropdownOptions;
        var statuses;

        this.attr('showStatusFilter', showStatusFilter);
        if (showStatusFilter) {
          statuses =
            this.attr('displayPrefs').getTreeViewStates(modelName);

          if (!statuses.length) {
            statuses = GGRC.Utils.State.getDefaultStatesForModel(modelName);
          }

          dropdownOptions = GGRC.Utils.State.getStatesForModel(modelName);
          dropdownOptions = dropdownOptions.map(function (option) {
            if (statuses.indexOf(option) > -1) {
              return {
                value: option,
                checked: true
              };
            }
            return {value: option};
          });

          this.attr('dropdown_options', dropdownOptions);
          this.attr('statusFilter', GGRC.Utils.State
            .statusFilter(statuses, '', this.attr('type')));

          this.attr('statuses', statuses);
        } else {
          this.attr('statuses', []);
          this.attr('statusFilter', '');
        }
      },
      saveStatusFilter: function () {
        var modelName = this.getModelName();
        this.displayPrefs.setTreeViewStates(
          modelName,
          can.makeArray(this.attr('statuses'))
        );
      }
    },
    events: {
      '{viewModel} totalObjects': function (scope, ev, totalObjects) {
        this.viewModel.attr('objectsPlural', totalObjects > 1);
      },
      '{viewModel} afterSearch': function (scope, ev, afterSearch) {
        if (!afterSearch) {
          this.viewModel.attr('totalObjects', 0);
        }
      },
      '{viewModel} type': function () {
        this.viewModel.setStatusFilter();
      },
      'multiselect-dropdown multiselect:closed': function (el, ev, selected) {
        var selectedStatuses = selected.map(function (item) {
          return item.value;
        });
        this.viewModel.attr('statuses', selectedStatuses);

        this.viewModel.attr('statusFilter', GGRC.Utils.State.statusFilter(
          selectedStatuses, '', this.viewModel.attr('type')));
        ev.stopPropagation();
      }
    }
  });
})(window.can, window.GGRC, window.CMS);
