'use strict';

/* Services */

angular.module('zk.admin.services', []).
  value('app.name', 'Zookeepr Admin').
  value('app.version', '0.1')

angular.module('zk.admin.person.services', []).
  factory('person', function($resource) {
    return $resource('/api/person/:personId', { personId:'@id' });
  });
