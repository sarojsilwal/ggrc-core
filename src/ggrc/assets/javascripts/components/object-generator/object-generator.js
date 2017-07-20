/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, $) {
  'use strict';

  /**
   * A component implementing a modal for mapping objects to other objects,
   * taking the object type mapping constraints into account.
   */
  GGRC.Components('objectGenerator', {
    tag: 'object-generator',
    template: can.view(GGRC.mustache_path +
      '/components/object-generator/object-generator.mustache'),
    viewModel: function (attrs, parentViewModel) {
      return GGRC.VM.ObjectOperationsBaseVM.extend({
        object: attrs.object,
        join_object_id: attrs.joinObjectId,
        type: attrs.type,
        relevantTo: parentViewModel.attr('relevantTo'),
        callback: parentViewModel.attr('callback'),
        useTemplates: true,
        useSnapshots: true,
        isLoadingOrSaving: function () {
          return this.attr('is_saving') ||
          this.attr('block_type_change') ||
          //  disable changing of object type while loading
          //  to prevent errors while speedily selecting different types
          this.attr('is_loading');
        }
      });
    },

    events: {
      inserted: function () {
        var self = this;
        this.viewModel.attr('selected').replace([]);
        this.viewModel.attr('entries').replace([]);

        this.setModel();

        self.viewModel.afterShown();
      },
      closeModal: function () {
        this.viewModel.attr('is_saving', false);
        this.element.find('.modal-dismiss').trigger('click');
      },
      '.modal-footer .btn-map click': function (el, ev) {
        var type = this.viewModel.attr('type');
        var object = this.viewModel.attr('object');
        var assessmentTemplate =
          this.viewModel.attr('assessmentTemplate');
        var instance = CMS.Models[object].findInCacheById(
          this.viewModel.attr('join_object_id'));

        ev.preventDefault();
        if (el.hasClass('disabled') ||
        this.viewModel.attr('is_saving')) {
          return;
        }

        this.viewModel.attr('is_saving', true);
        return this.viewModel.callback(this.viewModel.attr('selected'), {
          type: type,
          target: object,
          instance: instance,
          assessmentTemplate: assessmentTemplate,
          context: this
        });
      },
      setModel: function () {
        var type = this.viewModel.attr('type');

        this.viewModel.attr('model', this.viewModel.modelFromType(type));
      },
      '{viewModel} type': function () {
        this.viewModel.attr('filter', '');
        this.viewModel.attr('afterSearch', false);

        this.setModel();

        setTimeout(this.viewModel.onSubmit.bind(this.viewModel));
      },
      '{viewModel} assessmentTemplate': function (viewModel, ev, val, oldVal) {
        var type;
        if (_.isEmpty(val)) {
          return this.viewModel.attr('block_type_change', false);
        }

        val = val.split('-');
        type = val[1];
        this.viewModel.attr('block_type_change', true);
        this.viewModel.attr('type', type);
      }
    }
  });
})(window.can, window.can.$);
