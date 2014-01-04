'use strict';

/* Directives */


angular.module('zk.admin.directives', []).
  directive('appName', ['app.name', function(name) {
    return function(scope, elm, attrs) {
      elm.text(name);
    };
  }]).
  directive('appVersion', ['app.version', function(version) {
    return function(scope, elm, attrs) {
      elm.text(version);
    };
  }]);

