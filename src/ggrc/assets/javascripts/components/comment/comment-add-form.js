/*!
 Copyright (C) 2017 Google Inc.
 Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 */

(function (_, GGRC, can) {
  'use strict';

  var tag = 'comment-add-form';
  var template = can.view(GGRC.mustache_path +
    '/components/comment/comment-add-form.mustache');

  /**
   * A component that takes care of adding comments
   *
   */
  GGRC.Components('commentAddForm', {
    tag: tag,
    template: template,
    viewModel: {
      instance: {},
      sendNotifications: true,
      isSaving: false,
      isLoading: false,
      getCommentData: function () {
        var source = this.attr('instance');

        return {
          comment: source.attr('context'),
          send_notification: this.attr('sendNotifications'),
          context: source.context,
          assignee_type: GGRC.Utils.getAssigneeType(source),
          created_at: new Date(),
          modified_by: {type: 'Person', id: GGRC.current_user.id}
        };
      },
      updateComment: function (comment) {
        comment.mark_for_addition('related_objects_as_destination',
          this.attr('instance'));
        comment.attr(this.getCommentData());
        return comment;
      },
      onCommentCreated: function (e) {
        var comment = e.comment;
        this.attr('isSaving', true);
        comment = this.updateComment(comment);
        this.dispatch({type: 'beforeCreate', items: [comment.attr()]});
        comment.save()
          .always(function () {
            this.attr('isSaving', false);
            this.dispatch('afterCreate');
            this.attr('instance').dispatch('refreshInstance');
          }.bind(this));
      }
    }
  });
})(window._, window.GGRC, window.can);
