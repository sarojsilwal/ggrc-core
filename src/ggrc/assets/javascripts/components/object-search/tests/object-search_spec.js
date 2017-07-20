/*!
  Copyright (C) 2017 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('GGRC.Components.objectSearch', function () {
  'use strict';

  var Component;
  var events;
  var viewModel;
  var handler;

  beforeAll(function () {
    Component = GGRC.Components.get('objectSearch');
    events = Component.prototype.events;
  });
  beforeEach(function () {
    viewModel = new GGRC.Components.getViewModel('objectSearch')();
  });

  describe('viewModel() method', function () {
    it('returns object with function "isLoadingOrSaving"', function () {
      var result = Component.prototype.viewModel()();
      expect(result.isLoadingOrSaving).toEqual(jasmine.any(Function));
    });

    describe('isLoadingOrSaving() method', function () {
      it('returns true if it is loading', function () {
        viewModel.attr('is_loading', true);
        expect(viewModel.isLoadingOrSaving()).toEqual(true);
      });
      it('returns false if page is not loading, it is not saving,' +
      ' type change is not blocked and mapper is not loading', function () {
        viewModel.attr('is_loading', false);
        expect(viewModel.isLoadingOrSaving()).toEqual(false);
      });
    });
  });

  describe('"inserted" event', function () {
    var that;

    beforeEach(function () {
      viewModel.attr({
        afterShown: function () {}
      });
      that = {
        viewModel: viewModel,
        setModel: jasmine.createSpy('setModel')
      };
      handler = events.inserted;
    });

    it('calls setModel()', function () {
      handler.call(that);
      expect(that.setModel).toHaveBeenCalled();
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
    it('sets empty array to relevant if it is not in scope model',
      function () {
        spyOn(GGRC.Utils.Snapshots, 'isInScopeModel')
          .and.returnValue(false);
        handler.call(that);
        expect(viewModel.attr('relevant').length)
          .toEqual(0);
      });
  });

  describe('availableTypes() method', function () {
    it('correctly calls getMappingTypes', function () {
      var result;
      spyOn(GGRC.Mappings, 'getMappingTypes').and.returnValue('types');
      viewModel.attr('object', 'testObject');

      result = viewModel.availableTypes();
      expect(GGRC.Mappings.getMappingTypes).toHaveBeenCalledWith('testObject',
        ['TaskGroupTask', 'TaskGroup', 'CycleTaskGroupObjectTask'], []);
      expect(result).toEqual('types');
    });
  });
});
