'use strict';
var navRouting = [
  {
    heading: 'People',
    templateUrl: 'partials/person.html',
    controller: 'PersonCtrl',
    url: '/person',
    routes: []
  },
  {
    heading: 'Funding',
    templateUrl: 'partials/funding.html',
    controller: 'FundingCtrl',
    url: '/funding',
    routes: []
  },
  {
    heading: 'Invoices',
    templateUrl: 'partials/invoice.html',
    controller: 'InvoiceCtrl',
    url: '/invoice',
    routes: [
      {
        templateUrl: 'partials/invoice_new.html',
        controller: 'NewInvoiceCtrl',
        url: '/invoice/new',
        routes: []
      }
    ]
  },
  {
    heading: 'Fulfilment',
    templateUrl: 'partials/fulfilment.html',
    controller: 'FulfilmentCtrl',
    url: '/fulfilment',
    routes: []
  },
  {
    heading: 'Inventory',
    templateUrl: 'partials/inventory.html',
    controller: 'InventoryCtrl',
    url: '/inventory',
    routes: []
  },
  {
    heading: 'Vouchers',
    templateUrl: 'partials/voucher.html',
    controller: 'VoucherCtrl',
    url: '/voucher',
    routes: []
  },
  {
    heading: 'Check-in',
    templateUrl: 'partials/checkin.html',
    controller: 'CheckinCtrl',
    url: '/checkin',
    routes: []
  },
  {
    heading: 'Programme',
    templateUrl: 'partials/programme.html',
    controller: 'ProgrammeCtrl',
    url: '/programme',
    routes: []
  }
]

var allRoutes = [];
var addRoutes = function(element) {
  allRoutes.push({
    path: element.url,
    route: {
      templateUrl: element.templateUrl,
      controller: element.controller,
    }
  })
  element.routes.forEach(addRoutes)
}

navRouting.forEach(addRoutes)

// Declare app level module which depends on filters, and services
angular.module('zk.admin', [
  'ngRoute',
  'ngResource',
  'ui.bootstrap',
  'zk.admin.filters',
  'zk.admin.services',
  'zk.admin.directives',
  'zk.admin.controllers',
  'zk.admin.invoice',
]).
config([
  '$routeProvider',
  '$locationProvider',
  function($routeProvider, $locationProvider) {
    allRoutes.forEach(function(element) {
      $routeProvider.when(element.path, element.route)
    })
    $routeProvider.when ('/', {
        templateUrl: 'partials/home.html',
        controller: 'HomeCtrl'
    })
    $routeProvider.otherwise({redirectTo: '/'});
  }
]);
