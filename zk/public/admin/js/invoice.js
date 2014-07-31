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
  .filter('cents2dollars', function() { return cents2dollars })
  .service('products', function($http) {
    return $http.get('/product/json').then(
      function(response) {
        return response.data.r;
      }
    )
  })
  .controller('NewInvoiceCtrl', function ($scope, $filter, $routeParams, products) {
    // query params
    $scope.display = $routeParams.display;

    // Product List 
    $scope.product_list = products;

    // Used Products
    $scope.product_used = [];

    // Selected Product
    $scope.product_select;

    // Manual Description
    $scope.manual = {};
    $scope.manual.qty = 1;

    // Create empty Invoice Schema
    $scope.new_invoice = function() {
      $scope.invoice = {};
      var today = new Date();
      $scope.invoice.due_date = [today.getDate(), today.getMonth()+1, today.getFullYear()].join('/');
      $scope.invoice.items = [];
      $.each($scope.product_used, function(i, v) {
        $scope.product_list.splice(0, 0, v);
        $scope.product_used.splice(i, 1);
      })
    }

    // Refund Schema
    $scope.refund = {};
    $scope.refund.invoice_id = null;

    $scope.refund_invoice = function($event) {
      if ($scope.refund.invoice_id) {
        callback = function(response) {
          $scope.new_invoice();
          $.each(response.r.invoice.items, function(i, v) {
              response.r.invoice.items[i].qty = -v.qty;
              if (v.product_id) {
                product = $filter('filter')($scope.product_list, {'id': v.product_id})[0];
                $scope.product_list.splice($scope.product_list.indexOf(product), 1);
                $scope.product_used.splice(0,0,product);
              }
            }
          )
          $scope.invoice = response.r.invoice;
          $scope.$apply();
          console.log($scope.invoice);
        }
        $scope.get_invoice($event, callback, $scope.refund.invoice_id);
      }
    }

    $scope.get_invoice = function($event, callback, invoice_id) {
      $.get(invoice_id + '/get_invoice', callback);
    }

    // Check if we have been given a refund to process
    if ($scope.refund.invoice_id) {
      $scope.new_invoice();
      $scope.refund_invoice();
    // Otherwise create a new empty invoice
    } else {
      $scope.new_invoice();
      $scope.invoice.person_id = $routeParams.person_id || '';
    }

    // Processing Status
    $scope.processing = false;

    $scope.cost_sum = function() {
      var sum = 0;
      $.each(
        $scope.invoice.items, function(i,v) {
          sum += (parseInt(v.qty) || 0) * (parseInt(v.cost) || 0);
        }
      );
      return sum
    };

    $scope.add_line = function($event) {
      if (typeof $scope.product_select === "object") {
        // Create a new item and add it to the list
        item = {};
        item.description = $scope.product_select.category + " - " + $scope.product_select.description;
        item.cost = $scope.product_select.cost;
        item.product_id = $scope.product_select.id;
        item.qty = 1;
        $scope.invoice.items.push(item);

        // Push the item into the used list
        $scope.product_used.push($scope.product_select);

        // Remove the item from the product_list
        $scope.product_list.splice($scope.product_list.indexOf($scope.product_select), 1);
        $scope.product_select = null;
      }
    };

    $scope.add_manual = function() {
      $scope.invoice.items.push($scope.manual);
      $scope.manual = {}
    };

    $scope.remove_line = function(index) {
      if ($scope.invoice.items[index].product_id) {
        product = $filter('filter')($scope.product_used, {'id': $scope.invoice.items[index].product_id})[0];
        $scope.product_list.push(product);
      }
      $scope.invoice.items.splice(index, 1);
    }

    $scope.submit_invoice = function($event, callback) {
      if (! ($scope.invoice.person_id && $scope.invoice.due_date && $scope.invoice.items.length)) {
        $event.preventDefault();
        return false;
      }
      if ($scope.processing) {
        $event.preventDefault();
        return false;
      } else {
        $scope.processing = true;
      }
      $.post('', {invoice: JSON.stringify($scope.invoice)}, callback);
    }

    $scope.submit_payment = function($event, callback, invoice_id) {
      if($scope.processing) {
        $event.preventDefault();
        return false;
      } else {
        $scope.processing = true;
      }
      $.get(invoice_id + '/pay_invoice', callback);
    }
    $scope.submit_view_invoice = function($event) {
      callback = function(response) {
        $scope.processing = false;
        // Response in an invoice id
        console.log("response", response);
        window.location.href = response['r']['invoice_id'];
      };
      return $scope.submit_invoice($event, callback)
    }

    $scope.submit_new_invoice = function($event) {
      callback = function(response) {
        $scope.processing = false;
        // Response in an invoice id
        console.log("response", response);
        $scope.new_invoice();
      };
      return $scope.submit_invoice($event, callback)
    }

    $scope.submit_checkin_invoice = function($event) {
      callback = function(response) {
        $scope.processing = false;
        // Response in an invoice id
        console.log("response", response);
        // They have to pay by card... all done
        window.location.href = '/checkin?id=' + $scope.invoice.person_id;
      };
      return $scope.submit_invoice($event, callback)
    };

    $scope.submit_cash_checkin_invoice = function($event) {
      callback = function(response) {
        $scope.processing = false;
        // Response is an invoice id
        console.log("response", response);
        callback = function(response) {
          $scope.processing = false;
          console.log("response", response);
          window.location.href = '/checkin?id=' + $scope.invoice.person_id;
        };
        return $scope.submit_payment($event, callback, response['r']['invoice_id']);
      };
      return $scope.submit_invoice($event, callback)
    };
  });
