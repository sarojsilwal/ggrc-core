/*!
    Copyright (C) 2017 Google Inc.
    Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

(function (can) {
  'use strict';

  var INLINE_FORM_SAVE_DELAY = 1000;

  GGRC.Components('inlineFormControl', {
    tag: 'inline-form-control',
    viewModel: {
      instance: {},
      isSaving: false,
      pendingChanges: {},
      saveTimeoutHandler: {},
      autoSaveAfterSave: false,
      formSavedDeferred: can.Deferred().resolve(),

      saveChange: function () {
        var self = this;
        var instance = this.attr('instance');
        var pendingChanges = this.attr('pendingChanges');

        if (!can.Map.keys(pendingChanges).length) {
          this.attr('isSaving', false);
          return;
        }

        clearTimeout(this.attr('saveTimeoutHandler'));
        this.attr('isSaving', true);
        instance.attr(pendingChanges);
        this.attr('pendingChanges', {});

        instance.save().then(function () {
          if (self.attr('autoSaveAfterSave')) {
            self.attr('autoSaveAfterSave', false);
            setTimeout(self.saveChange.bind(self));
          }

          self.attr('formSavedDeferred').resolve();
        })
        .always(function () {
          self.attr('isSaving', false);
        });
      },
      saveInlineForm: function (args) {
        var value = args.value;
        var propName = args.propName;
        this.attr('pendingChanges').attr(propName, value);
        this.attr('formSavedDeferred', can.Deferred());

        if (this.attr('isSaving')) {
          this.attr('autoSaveAfterSave', true);
          return;
        }

        this.attr(
          'saveTimeoutHandler',
          setTimeout(this.saveChange.bind(this), INLINE_FORM_SAVE_DELAY)
        );
      }
    }
  });
})(window.can);
