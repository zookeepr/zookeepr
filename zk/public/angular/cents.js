define(['angular'], function(angular) {
	var module_name = 'cents';
	angular.module(module_name, [])
		.directive('cents', cents_directive)
		.filter('dollars2cents', function() { return dollars2cents })
		.filter('cents2dollars', function() { return cents2dollars });
	return module_name;
});

function cents2dollars(text) {
	if (text == "-") {
		return text;
	} else {
		return (text || 0) / 100;
	}
}

function dollars2cents(text) {
	if (text == "-") {
		return text;
	} else {
		return (text || 0) * 100;
	}
}

function cents_directive() {
	return {
		// restrict: 'A',
		require: 'ngModel',
		link: function(scope, element, attr, ngModel) {
			ngModel.$formatters.push(cents2dollars);
			ngModel.$parsers.push(dollars2cents);
		}
	};
}
