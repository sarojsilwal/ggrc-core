/*!
    Copyright (C) 2017 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

(function (can) {
  'use strict';

  var tpl = can.view(GGRC.mustache_path +
    '/components/assessment/info-pane/confirm-inline-control-title.mustache');

  GGRC.Components('confirmInlineControlTitle', {
    tag: 'confirm-inline-control-title',
    template: tpl,
    viewModel: {
      instance: {},
      setInProgress: null,
      editMode: false,
      isEditIconDenied: false,
      onStateChangeDfd: can.Deferred().resolve(),
      openInlineEdit: function (el) {
        this.attr('onStateChangeDfd').then(function () {
          if (this.isInProgress()) {
            this.dispatch('setEditModeInline');
          }
        }.bind(this));
      },
      isInProgress: function () {
        return this.attr('instance.status') === 'In Progress';
      },
      showConfirm: function () {
        var self = this;
        var confirmation = can.Deferred();
        GGRC.Controllers.Modals.confirm({
          modal_title: 'Confirm moving Assessment to "In Progress"',
          modal_description: 'You are about to move Assesment from "' +
            this.instance.status +
            '" to "In Progress" - are you sure about that?',
          button_view: GGRC.mustache_path + '/modals/prompt_buttons.mustache'
        }, confirmation.resolve, confirmation.reject);

        confirmation.then(function (data) {
          self.dispatch('setInProgress');
          self.openInlineEdit();
        });
      },
      setEditModeInline: function () {
        if (!this.isInProgress()) {
          this.showConfirm();
          return;
        }

        // send 'isLastOpenInline' when inline is opening without confirm
        this.dispatch({
          type: 'setEditModeInline',
          isLastOpenInline: true
        });
      }
    }
  });
})(window.can);
