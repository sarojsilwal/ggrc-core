/*!
  Copyright (C) 2017 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('GGRC.Components.mapperToolbar', function () {
  'use strict';

  var viewModel;

  beforeEach(function () {
    var Component = GGRC.Components.get('mapperToolbar');
    var init = Component.prototype.viewModel.init;
    Component.prototype.viewModel.init = undefined;
    viewModel = GGRC.Components.getViewModel('mapperToolbar');
    viewModel.attr({
      type: 'Control'
    });
    Component.prototype.viewModel.init = init;
    viewModel.init = init;
  });

  describe('init() method', function () {
    beforeEach(function () {
      spyOn(CMS.Models.DisplayPrefs, 'getSingleton')
        .and.returnValue($.Deferred().resolve('mockPrefs'));
      spyOn(viewModel, 'setStatusFilter');
    });

    it('sets displayPrefs to viewModel', function () {
      viewModel.init();
      expect(viewModel.attr('displayPrefs')).toEqual('mockPrefs');
    });

    it('calls setStatusFilter()', function (done) {
      viewModel.init();

      setTimeout(function () {
        expect(viewModel.setStatusFilter).toHaveBeenCalled();
        done();
      });
    });
  });

  describe('onSubmit() method', function () {
    beforeEach(function () {
      spyOn(viewModel, 'dispatch');
      spyOn(viewModel, 'saveStatusFilter');
    });

    it('should dispatch submit event', function () {
      viewModel.onSubmit();
      expect(viewModel.dispatch)
        .toHaveBeenCalledWith('submit');
    });

    it('calls saveStatusFilter if showStatusFilter is true', function () {
      viewModel.attr('showStatusFilter', true);
      viewModel.onSubmit();
      expect(viewModel.saveStatusFilter)
        .toHaveBeenCalled();
    });
  });

  describe('onReset() method', function () {
    beforeEach(function () {
      spyOn(viewModel, 'dispatch');
    });

    it('viewModel.filter should be ""', function () {
      viewModel.attr('filter', 'text');
      viewModel.onReset();
      expect(viewModel.attr('filter')).toEqual('');
    });

    it('viewModel.statuses should be []', function () {
      viewModel.attr('statuses', [1, 2, 3]);
      viewModel.onReset();
      expect(viewModel.attr('statuses').length).toEqual(0);
    });

    it('viewModel.statusFilter should be ""', function () {
      viewModel.attr('statusFilter', 'status');
      viewModel.onReset();
      expect(viewModel.attr('statusFilter')).toEqual('');
    });

    it('should dispatch submit event', function () {
      viewModel.onReset();
      expect(viewModel.dispatch)
        .toHaveBeenCalledWith('submit');
    });
  });

  describe('getModelName() method', function () {
    it('returns model name', function () {
      var result;
      viewModel.attr('type', 'Program');
      result = viewModel.getModelName();
      expect(result).toEqual(CMS.Models.Program.model_singular);
    });
  });

  describe('setStatusFilter() method', function () {
    var dropdownOptions = [1, 2, 3];
    var statuses = [1];
    var expectedResult = jasmine.objectContaining([
      jasmine.objectContaining({
        value: 1,
        checked: true
      })
    ]);

    beforeEach(function () {
      spyOn(viewModel, 'getModelName')
        .and.returnValue('program');
      viewModel.attr('displayPrefs', {
        getTreeViewStates: function () {
          return statuses;
        }
      });
      spyOn(GGRC.Utils.State, 'statusFilter')
        .and.returnValue('mockStatus');
      spyOn(GGRC.Utils.State, 'getStatesForModel')
        .and.returnValue(dropdownOptions);
    });

    it('sets viewModel.showStatusFilter', function () {
      spyOn(GGRC.Utils.State, 'hasState')
        .and.returnValue(false);
      viewModel.setStatusFilter();
      expect(viewModel.attr('showStatusFilter')).toEqual(false);
    });

    it('should update satuses if showStatusFilter is false', function () {
      spyOn(GGRC.Utils.State, 'hasState')
        .and.returnValue(false);
      viewModel.setStatusFilter();
      expect(viewModel.attr('statuses').length).toEqual(0);
    });

    it('should update statusFilter if showStatusFilter is false', function () {
      spyOn(GGRC.Utils.State, 'hasState')
        .and.returnValue(false);
      viewModel.setStatusFilter();
      expect(viewModel.attr('statusFilter')).toEqual('');
    });

    it('should update dropdown_options if showStatusFilter is true',
      function () {
        spyOn(GGRC.Utils.State, 'hasState')
          .and.returnValue(true);
        viewModel.setStatusFilter();
        expect(viewModel.attr('dropdown_options'))
          .toEqual(expectedResult);
      });

    it('should update statusFilter if showStatusFilter is true',
      function () {
        spyOn(GGRC.Utils.State, 'hasState')
          .and.returnValue(true);
        viewModel.setStatusFilter();
        expect(viewModel.attr('statusFilter')).toEqual('mockStatus');
      });

    it('should update statuses if showStatusFilter is true',
      function () {
        spyOn(GGRC.Utils.State, 'hasState')
          .and.returnValue(true);
        viewModel.setStatusFilter();
        expect(viewModel.attr('statuses'))
          .toEqual(jasmine.objectContaining(statuses));
      });
  });

  describe('saveStatusFilter() method', function () {
    var statuses = [1, 2, 3];
    beforeEach(function () {
      viewModel.attr('statuses', statuses);
      viewModel.attr('displayPrefs', {
        setTreeViewStates: function () {}
      });
      spyOn(viewModel, 'getModelName')
        .and.returnValue('mockName');
      spyOn(viewModel.displayPrefs, 'setTreeViewStates');
    });

    it('should call displayPrefs.setTreeViewStates', function () {
      viewModel.saveStatusFilter();
      expect(viewModel.displayPrefs.setTreeViewStates)
        .toHaveBeenCalledWith('mockName', jasmine.objectContaining(statuses));
    });
  });
});
