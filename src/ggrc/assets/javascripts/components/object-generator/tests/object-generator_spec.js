/*!
  Copyright (C) 2017 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('GGRC.Components.objectGenerator', function () {
  'use strict';

  var Component;
  var events;
  var viewModel;
  var handler;

  beforeAll(function () {
    Component = GGRC.Components.get('objectGenerator');
    events = Component.prototype.events;
  });

  describe('viewModel() method', function () {
    var parentViewModel;
    beforeEach(function () {
      parentViewModel = new can.Map();
    });
    it('returns object with function "isLoadingOrSaving"', function () {
      var result = new Component.prototype.viewModel({}, parentViewModel)();
      expect(result.isLoadingOrSaving).toEqual(jasmine.any(Function));
    });

    describe('isLoadingOrSaving() method', function () {
      beforeEach(function () {
        viewModel = new Component.prototype.viewModel({}, parentViewModel)();
      });
      it('returns true if it is saving', function () {
        viewModel.attr('is_saving', true);
        expect(viewModel.isLoadingOrSaving()).toEqual(true);
      });
      it('returns true if type change is blocked', function () {
        viewModel.attr('block_type_change', true);
        expect(viewModel.isLoadingOrSaving()).toEqual(true);
      });
      it('returns true if it is loading', function () {
        viewModel.attr('is_loading', true);
        expect(viewModel.isLoadingOrSaving()).toEqual(true);
      });
      it('returns false if page is not loading, it is not saving,' +
      ' type change is not blocked and it is not loading', function () {
        viewModel.attr('is_saving', false);
        viewModel.attr('block_type_change', false);
        viewModel.attr('is_loading', false);
        expect(viewModel.isLoadingOrSaving()).toEqual(false);
      });
    });
  });

  describe('"inserted" event', function () {
    var that;

    beforeEach(function () {
      viewModel.attr({
        selected: [1, 2, 3],
        entries: [3, 2, 1],
        afterShown: function () {}
      });
      that = {
        viewModel: viewModel,
        setModel: jasmine.createSpy('setModel')
      };
      handler = events.inserted;
    });

    it('sets empty array to selected', function () {
      handler.call(that);
      expect(viewModel.attr('selected').length)
        .toEqual(0);
    });
    it('sets empty array to entries', function () {
      handler.call(that);
      expect(viewModel.attr('entries').length)
        .toEqual(0);
    });
    it('calls setModel()', function () {
      handler.call(that);
      expect(that.setModel).toHaveBeenCalled();
    });
  });

  describe('"closeModal" event', function () {
    var element;
    var spyObj;

    beforeEach(function () {
      viewModel.attr({});
      spyObj = {
        trigger: function () {}
      };
      element = {
        find: function () {
          return spyObj;
        }
      };
      spyOn(spyObj, 'trigger');
      handler = events.closeModal;
    });

    it('sets false to is_saving', function () {
      viewModel.attr('is_saving', true);
      handler.call({
        element: element,
        viewModel: viewModel
      });
      expect(viewModel.attr('is_saving')).toEqual(false);
    });
    it('dismiss the modal', function () {
      handler.call({
        element: element,
        viewModel: viewModel
      });
      expect(spyObj.trigger).toHaveBeenCalledWith('click');
    });
  });

  describe('".modal-footer .btn-map click" handler', function () {
    var that;
    var event;
    var element;
    var callback;

    beforeEach(function () {
      callback = jasmine.createSpy().and.returnValue('expectedResult');
      viewModel.attr({
        callback: callback,
        type: 'type',
        object: 'Program',
        assessmentTemplate: 'template',
        join_object_id: '123',
        selected: []
      });
      spyOn(CMS.Models.Program, 'findInCacheById')
        .and.returnValue('instance');
      event = {
        preventDefault: function () {}
      };
      element = $('<div></div>');
      handler = events['.modal-footer .btn-map click'];
      that = {
        viewModel: viewModel,
        closeModal: jasmine.createSpy()
      };
      spyOn(window, 'RefreshQueue')
        .and.returnValue({
          enqueue: function () {
            return {
              trigger: jasmine.createSpy()
                .and.returnValue(can.Deferred().resolve())
            };
          }
        });
      spyOn($.prototype, 'trigger');
    });

    it('does nothing if element has class "disabled"', function () {
      var result;
      element.addClass('disabled');
      result = handler.call(that, element, event);
      expect(result).toEqual(undefined);
    });

    it('sets true to is_saving and returns callback', function () {
      var result;
      result = handler.call(that, element, event);
      expect(viewModel.attr('is_saving')).toEqual(true);
      expect(result).toEqual('expectedResult');
      expect(callback.calls.argsFor(0)[0].length)
        .toEqual(0);
      expect(callback.calls.argsFor(0)[1]).toEqual({
        type: 'type',
        target: 'Program',
        instance: 'instance',
        assessmentTemplate: 'template',
        context: that
      });
    });
  });

  describe('"setModel" handler', function () {
    beforeEach(function () {
      viewModel.attr({
        modelFromType: function () {}
      });
      spyOn(viewModel, 'modelFromType')
        .and.returnValue('mockModel');
      handler = events.setModel;
    });
    it('sets model to model', function () {
      handler.call({viewModel: viewModel});
      expect(viewModel.attr('model')).toEqual('mockModel');
    });
  });

  describe('"{viewModel} type" handler', function () {
    var that;
    beforeEach(function () {
      viewModel.attr({
        relevant: [1, 2, 3],
        onSubmit: function () {}
      });
      that = {
        viewModel: viewModel,
        setModel: jasmine.createSpy()
      };
      handler = events['{viewModel} type'];
    });

    it('sets empty string to filter', function () {
      handler.call(that);
      expect(viewModel.attr('filter')).toEqual('');
    });
    it('sets false to afterSearch', function () {
      handler.call(that);
      expect(viewModel.attr('afterSearch')).toEqual(false);
    });
    it('calls setModel()', function () {
      handler.call(that);
      expect(that.setModel).toHaveBeenCalled();
    });
  });

  describe('"{viewModel} assessmentTemplate" handler', function () {
    beforeEach(function () {
      viewModel.attr({});
      handler = events['{viewModel} assessmentTemplate'];
    });

    it('sets false to block_type_change if value is empty',
      function () {
        handler.call({viewModel: viewModel});
        expect(viewModel.attr('block_type_change'))
          .toEqual(false);
      });
    it('sets true to block_type_change if value is not empty',
      function () {
        handler.call({viewModel: viewModel}, viewModel, {}, 'mock-value');
        expect(viewModel.attr('block_type_change'))
          .toEqual(true);
      });
    it('sets type to type if value is not empty',
      function () {
        handler.call({viewModel: viewModel}, viewModel, {}, 'mock-value');
        expect(viewModel.attr('type'))
          .toEqual('value');
      });
  });
});
