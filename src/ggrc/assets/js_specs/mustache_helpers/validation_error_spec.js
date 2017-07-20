/*!
  Copyright (C) 2017 Google Inc.
  Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
*/

describe('can.mustache.helper.validation_error', function () {
  'use strict';

  var helper;
  var fakeOptions;

  beforeAll(function () {
    helper = can.Mustache._helpers.validation_error.fn;
  });

  beforeEach(function () {
    fakeOptions = {
      fn: jasmine.createSpy('options.fn'),
      inverse: jasmine.createSpy('options.inverse'),
      contexts: {
        add: jasmine.createSpy('contexts.add')
      }
    };
  });

  it('renders the "truthy" block if there are validation errors for the ' +
    'property',
    function () {
      var validationErrors = {
        'property_name.1': ['invalid value']
      };
      helper(validationErrors, 'property_name.1', fakeOptions);
      expect(fakeOptions.fn).toHaveBeenCalled();
    }
  );

  it('adds the errors list to the scope if there are validation errors for ' +
    'the property',
    function () {
      var validationErrors = {
        'property_name.1': ['invalid  date format'],
        'property_name.4': ['value is too short', 'not a number']
      };
      helper(validationErrors, 'property_name.4', fakeOptions);
      expect(fakeOptions.contexts.add).toHaveBeenCalledWith(
        {errors: ['value is too short', 'not a number']}
      );
    }
  );

  it('renders the "falsy" block if there are no validation errors for the ' +
    'property',
    function () {
      var validationErrors = {
        'property_name.4': ['invalid value']
      };
      helper(validationErrors, 'property_name', fakeOptions);
      expect(fakeOptions.inverse).toHaveBeenCalled();
    }
  );
});
