/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (GGRC, can) {
  'use strict';

  var tag = 'attach-button';
  var template = can.view(GGRC.mustache_path +
    '/components/assessment/attach-button.mustache');

  GGRC.Components('attachButton', {
    tag: tag,
    template: template,
    viewModel: {
      instance: {},
      isAttachActionDisabled: false,
      onBeforeCreate: function (event) {
        var items = event.items;
        this.dispatch({type: 'beforeCreate', items: items});
      },
      confirmationCallback: function () {
        var confirmation = null;

        if (this.attr('instance') instanceof CMS.Models.Assessment &&
            this.attr('instance.status') !== 'In Progress') {
          confirmation = can.Deferred();
          GGRC.Controllers.Modals.confirm({
            modal_title: 'Confirm moving Assessment to "In Progress"',
            modal_description: 'You are about to move Assesment from "' +
              this.instance.status +
              '" to "In Progress" - are you sure about that?',
            button_view: GGRC.mustache_path + '/modals/prompt_buttons.mustache'
          }, confirmation.resolve, confirmation.reject);
          return confirmation.promise();
        }

        return confirmation;
      },
      itemsUploadedCallback: function () {
        this.dispatch('refreshEvidences');

        if (this.attr('instance')) {
          this.attr('instance').dispatch('refreshInstance');
        }
      }
    }
  });
})(window.GGRC, window.can);
