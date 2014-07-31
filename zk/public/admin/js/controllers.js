'use strict';

/* Controllers */

angular.module('zk.admin.controllers', []).
  controller('TabCtrl', function($scope, $route, $location) {
    $scope.active = function (path) {
      return ($location.path() == path) ? 'active' : '';
    };
    $scope.tabs = navRouting;
    $scope.$route = $route;
  }).
  controller('PersonCtrl', function($scope, person) {
    $scope.people = person.query();
  }).
  controller('PersonDetailCtrl', function($scope) {

  }).
  controller('CheckinCtrl', function($scope, $http, $modal, $routeParams) {
    $("body").on('keyup', '#search', function() { 
	setTimeout( function() { 
		if ($("#search").next().find('li').length == 1) { 
			$($("#search").next().find('li')[0]).click() 
		} 
	}, 1000) 
    })
    
    $scope.search_select = function() {
        var person = $scope.search_input;
        $scope.loadPerson(person.id);
        $scope.addHistory(person);
        $scope.search_input = '';
    };

    $scope.history = []

    $scope.addHistory = function(person) {
        $scope.history = $scope.history.filter(function(element, index) {
          return !(element.id == person.id);
        })
        $scope.history.unshift(person);
        $scope.history.splice(5, 1);
    };

    $scope.person = {};

    $scope.findPerson = function(query) {
      return $http.get('/checkin/lookup', { params: { q: query } })
        .then(function(response) {
          return response.data.r;
        })
    };

    $scope.loadPerson = function(personId) {
      $http.get('/admin/generate_fulfilment').success(function() {
        $http.get('/checkin/person_data', { params: { id: personId } })
          .then(function(response) {
            $scope.person = response.data;
            $scope.blocks = response.data.notes.filter(function(element, index) {
              return element.block;
            })
            if ($scope.blocks.length) {
              $scope.block();
              $scope.person = {};
            }
          });
      });
    };

    $scope.block = function() {
      var modalInstance = $modal.open({
        templateUrl: 'partials/checkin_block.html',
        controller: 'CheckinBlockCtrl',
        resolve: {
          person: function() { return $scope.person },
          blocks: function() { return $scope.blocks },
        }
      });
    }

    $scope.badge_action = function($event, fulfilment) {
      $http.get('/fulfilment/' + fulfilment.id + '/badge_print').success(function() {
        $scope.loadPerson($scope.person.id);
      });
    }

    $scope.swag_action = function($event, fulfilment) {
      $http.get('/fulfilment/' + fulfilment.id + '/swag_give').success(function() {
        $scope.loadPerson($scope.person.id);
      });
    }

    if($routeParams.id) {
       $scope.loadPerson($routeParams.id);
    }

  }).
  controller('CheckinBlockCtrl', function($scope, $modalInstance, person, blocks) {
    $scope.person = person;
    $scope.blocks = blocks
    $scope.close = function() {
      $modalInstance.dismiss('close');
    };
  });
