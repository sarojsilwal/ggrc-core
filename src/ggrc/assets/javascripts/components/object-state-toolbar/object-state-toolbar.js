/*!
 Copyright (C) 2017 Google Inc., authors, and contributors
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (can, GGRC) {
  'use strict';

  var tag = 'object-state-toolbar';
  var tpl = can.view(GGRC.mustache_path +
    '/components/object-state-toolbar/object-state-toolbar.mustache');
  // Helper function - might be some util/helpers method
  function checkIsCurrentUserVerifier(verifiers) {
    return verifiers
      .filter(function (verifier) {
        return verifier.email === GGRC.current_user.email;
      }).length;
  }
  /**
   * Object State Toolbar Component allowing Object state modification
   */
  GGRC.Components('objectStateToolbar', {
    tag: tag,
    template: tpl,
    viewModel: {
      define: {
        updateState: {
          get: function () {
            return this.attr('hasVerifiers') ? 'Ready for Review' : 'Completed';
          }
        },
        isCurrentUserVerifier: {
          get: function () {
            return checkIsCurrentUserVerifier(this.attr('verifiers'));
          }
        },
        hasVerifiers: {
          get: function () {
            return this.attr('verifiers').length;
          }
        },
        hasErrors: {
          get: function () {
            return this.attr('instance.preconditions_failed') ||
              this.attr('instance.hasValidationErrors');
          }
        },
        isDisabled: {
          get: function () {
            return !!this.attr('instance._disabled') ||
              this.attr('hasErrors') ||
              this.attr('instance.isPending');
          }
        }
      },
      verifiers: [],
      instance: {},
      isInProgressOrNotStarted: function () {
        return this.attr('instance.status') === 'In Progress' ||
          this.attr('instance.status') === 'Not Started';
      },
      isInProgress: function () {
        return this.attr('instance.status') === 'In Progress';
      },
      isInReview: function () {
        return this.attr('instance.status') === 'Ready for Review';
      },
      changeState: function (newState, isUndo) {
        newState = newState || this.attr('updateState');
        this.dispatch({
          type: 'onStateChange',
          state: newState,
          undo: isUndo
        });
      }
    }
  });
})(window.can, window.GGRC);
