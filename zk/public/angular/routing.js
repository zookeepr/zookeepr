/* Custom routing
 * ==============
 *
 * This was initially implemented using angular-route.js but it was messy
 * with much hacking, mostly to disable features.
 *
 * Our use case is unusual.
 * 1. We want to load content dynamically based on the called URL.
 * 2. We do not want to rewrite links to implement a single page website.
 * 3. URL is pre-sanitised by serverside route map.
 *
 * All the existing solutions required duplicating the serverside route map
 * and disabling the single page navigation feature. It is cleaner this way.
 *
 * Implementation uses dynamic loading of the controller and partial. This
 * requires delaying Angular's initialisation until the controller is loaded.
 *
 * RequireJS
 * ---------
 *
 * The RequireJS library provides a mechanism to load javascript files from
 * javascript. Each javascript file can specify dependencies and requirejs
 * acts like a package manager ensuring that they are all met before
 * continuing. It does this in a nicely optimised way. RequireJS has traction
 * in getting its dependency specification adopted as a defacto standard.
 *
 * We use RequireJS because it nicely solves the thorny problem of how to load
 * controller specific dependancies. That is if we dynamically load ctrl_A and
 * it requires directive_B how do we ensure that the directive is known about
 * and loaded.
 *
 * Since it is here we use it for loading all the other Javascript too.
 *
 * The use of RequireJS does come with a price. All js files must provide a
 * module, and define its dependencies, even if they are empty. We use the
 * angular.module framework and let angular stitch all the files together.
 *
 * The framework also provides tools to minify and combine the javascript
 * files in the future.
 *
 * A good example of combining RequireJS and Angular is at
 * https://github.com/tastejs/todomvc/tree/gh-pages/examples/angularjs_require
 *
 * Custom Directive
 * ----------------
 *
 * A custom directive, dynamic-include, has been created to power the angular
 * side of the dynamic loading. This is a dumbed down version of ng-view from
 * angular-route.
 *
 * The first problem is that our loaded controller has to be injected into
 * the system. Angular doesn't make this simple, options are explored at
 * http://stackoverflow.com/a/21204497/2438650. Initially I went with the
 * third option and injected the controller into a div, ng-include was then
 * used to pull the content in.
 *
 * The downside to this method is that ng-include creates its own scope. So
 * the controller and scope is one level away from the content. This is managable,
 * the content's scope inherits from the parent one. But this exposes all sorts
 * of messy javascript inheritance issues that are difficult for a new user to
 * work with.
 *
 * The cleaner long term solution was to create a custom directive. This directive
 * does the include and creates the scope and powers up the controller.
 *
 * The directive is not designed to allow the content or controller to change once
 * loaded.
 *
 * To use
 * ------
 *
 * 1. Identify the path you wish to use, I will refer to it as $path
 * 2. In the Pylons controller for $path, return render('/angular.mako')
 * 3. Create an angular partial in /zk/public/$path.html
 * 4. Create an angular controller called ctrl in /zk/public/$path.js
 *
 * The controller must be of the format:
 *   define(['angular'], function (angular) {
 *     var module_name = 'change_config';
 *     angular.module(module_name, [JsonTextDirective])
 *     .controller(module_name, ['$scope', function($scope) {
 *       etcetera
 *     }]);
 *     return module_name;
 *   });
 *
 * An example implementation is at $path = admin/change_config
 */

// Find the request path
if(!document.baseURI.length)
	throw new Error('base must be defined');
if(window.location.href.indexOf(document.baseURI) != 0)
	throw new Error('Location must be relative to base');
var request = window.location.href.substr(document.baseURI.length);

require.config({
	baseUrl : "/angular",
	// enforceDefine: true, /* TODO: ngSanitize not working, doesn't export anything */
	waitSeconds: 0, // Disable loading timeout - server is sometimes slow
	paths : {
		"jquery"  : [
			"https://ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery",
			"https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.4/jquery",
			"https://ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery.min",
			"https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.4/jquery.min",
		],
		"angular" : [
			"https://ajax.googleapis.com/ajax/libs/angularjs/1.3.15/angular",
			"https://cdnjs.cloudflare.com/ajax/libs/angular.js/1.3.15/angular",
			"https://ajax.googleapis.com/ajax/libs/angularjs/1.3.15/angular.min",
			"https://cdnjs.cloudflare.com/ajax/libs/angular.js/1.3.15/angular.min",
		],
		"ngSanitize" : [
			'https://ajax.googleapis.com/ajax/libs/angularjs/1.3.15/angular-sanitize',
			"https://cdnjs.cloudflare.com/ajax/libs/angular.js/1.3.15/angular-sanitize",
			'https://ajax.googleapis.com/ajax/libs/angularjs/1.3.15/angular-sanitize.min',
			"https://cdnjs.cloudflare.com/ajax/libs/angular.js/1.3.15/angular-sanitize.min",
		],
	},
	shim : {
		"jquery"    : { exports: '$'},
		"angular"   : { exports: "angular",    deps: ["jquery" ] },
		"ngSanitize": { exports: 'ngSanitize', deps: ['angular'] },
	}
});

define([ "angular" ], function(angular) {
	// Initialise angular so that it can be used by the controller
	require(['/'+request+'.js'], function(ctrl) {
		var zk = angular.module('zk', [ctrl]);

		zk.config(['$compileProvider', function($compileProvider) {
			$compileProvider.debugInfoEnabled(true);
		}]);

		zk.directive('dynamicInclude', directive_dynamic_include);

		zk.run(['$rootScope', '$controller', function($rootScope, $controller) {
			// Save request string and new controller for use by angular
			$rootScope.request = request;
			$rootScope.loaded_ctrl = ctrl;
		}]);

		// Now everything is loaded we can start angular
		angular.element(document).ready(function() {
			angular.bootstrap(document, ['zk']);
		});
	});
});

function directive_dynamic_include($templateRequest, $compile, $controller, $parse) {
		return {
			restrict: 'E',
			terminal: true,
			priority: 1000,
			link: function(scope, $element, attr){
				var templatePath = $parse(attr.include)(scope);

				$templateRequest(templatePath).then(function(response) {
					// Pull in the new content
					$element.html(response);
					var link = $compile($element.contents());

					// Create the controller
					var ctrl_scope = scope.$new();
					var ctrl_name = $parse(attr.controller)(scope);
					var controller = $controller(ctrl_name, {'$scope': ctrl_scope});

					// Connect the controller to the content
					$element.data('$ngControllerController', controller);
					$element.children().data('$ngControllerController', controller);

					// Bind it all together
					link(ctrl_scope);
				});
			}
		};

}
