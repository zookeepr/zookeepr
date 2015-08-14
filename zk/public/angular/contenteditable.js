'use strict';
/* Directive to bind model to contenteditable
 *
 * Based off https://docs.angularjs.org/api/ng/type/ngModel.NgModelController#custom-control-example
 */

define(['angular', 'ngSanitize'], function (angular, sanitize) {
	var module_name = 'contenteditable';
	angular.module(module_name, [])
	.directive('contenteditable', ['$sce', function ($sce) {
		return {
			restrict: 'A', // only activate on element attribute
			require: '?ngModel', // get a hold of NgModelController
			link: function(scope, element, attrs, ngModel) {
				if (!ngModel) return; // do nothing if no ng-model

				// Specify how UI should be updated
				ngModel.$render = function() {
					// TODO: Currently we are unsafe so $sce complains
					// Messy to become safe using JSON objects
					// element.html($sce.getTrustedHtml(ngModel.$viewValue || ''));
					element.html(ngModel.$viewValue);
				};

				// Listen for change events to enable binding
				element.on('blur keyup change', function() {
					scope.$evalAsync(read);
				});
				read(); // initialize

				// Write data to the model
				function read() {
					var html = element.html();
					// When we clear the content editable the browser leaves a <br> behind
					// If strip-br attribute is provided then we strip this out
					if ( attrs.stripBr && html == '<br>' ) {
						html = '';
					}
					// Convert br tags to newlines - Hitting enter throws BRs :(
					html = html.replace(/<\s*br(\s[^>]*)?>/g, "\n");
					ngModel.$setViewValue(html);
				}
			}
		};
	}]);
	return module_name;
});
