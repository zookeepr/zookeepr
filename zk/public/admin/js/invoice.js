'use strict';

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

angular.module('zk.admin.invoice', [])
  .directive('cents', function() {
    return {
      require: 'ngModel',
      link: function(scope, element, attr, ngModel) {
        ngModel.$formatters.push(cents2dollars);
        ngModel.$parsers.push(dollars2cents);
      }
    };
  })
  .filter('dollars2cents', function() { return dollars2cents })
  .filter('cents2dollars', function() { return cents2dollars });
