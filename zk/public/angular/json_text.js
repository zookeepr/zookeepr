'use strict';

define(['angular'], function (angular) {
	var module_name = 'json_text';
	angular.module(module_name, [])
	.directive('jsonText', [function () {
		return {
			require: 'ngModel',
			link: function (scope, elem, attrs, ngModel) {
				var toView = function (val) {
					return typeof val == 'string' ? val : angular.toJson(val,2);
				};
				
				var toModel = function (val) {
					if (val[0] == '"' || val[0] == '{' || val[0] == '[') {
						try {
							return angular.fromJson(val);
						} catch (e) {
							console.log("Bad JSON", val, e);
							ngModel.$setValidity('json', false);
							return undefined;
						}
					} else {
						return val;
					}
				};

				// Note: We must be the first parser, stringify will bork us
				ngModel.$parsers.push(toModel);
				ngModel.$formatters.unshift(toView);
			}
		};
	}]);
	return module_name;
});
