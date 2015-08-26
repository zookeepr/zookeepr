// 'use strict';

define([ 'angular', 'contenteditable', 'json_text' ], function (angular, ContenteditableDirective, JsonTextDirective) {
	var module_name = 'change_config';
	angular.module(module_name, [ContenteditableDirective, JsonTextDirective])
	.controller(module_name, ['$scope', '$http', '$sce', function($scope, $http, $sce) {
		$scope.contentLoaded = false;
		$scope.data = [];

		$http.get('/admin/config').then(function(response) {
			$scope.data = response.data;
			$scope.contentLoaded = true;
		});

		$scope.$watch("data", function (new_val, old_val) {
			// Ignore changes until data has been initialised properly
			if (old_val.length == 0) {
				return;
			}

			// Find the change, could be complex object, potentially multiple changes
			for(var i=0; i < old_val.length; i++) {
				if (!angular.equals(old_val[i]['value'], new_val[i]['value'])) {
					console.log("Change", old_val[i]['value'], "->", new_val[i]['value']);
					$scope.update(new_val[i]);
				}
			}
		}, true);

		$scope.update = function(data_row) {
			data_row.response = "";

			if (typeof data_row.value === 'undefined') {
				// JSON parse error
				data_row.response = "error";
				return;
			}

			$http.put('/admin/config', data_row).
				success(function(data, status, headers, config) {
					data_row.response = "success";
				}).
				error(function(data, status, headers, config) {
					data_row.response = "error";
				});
		};
	}]);
	return module_name;
});
