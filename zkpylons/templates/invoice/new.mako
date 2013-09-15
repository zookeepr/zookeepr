<!doctype html>
<html ng-app="invoice">
<head>
<title>Create Invoice</title>
<script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js"></script>
<script src="//ajax.googleapis.com/ajax/libs/angularjs/1.0.3/angular.min.js"></script>
<script src="/bootstrap/js/bootstrap.js"></script>
<link href="/bootstrap/css/bootstrap.min.css" rel="stylesheet" media="screen">


<script type="text/javascript">
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

angular.module('invoice', [])
  .directive('cents', function() {
    return {
      // restrict: 'A',
      require: 'ngModel',
      link: function(scope, element, attr, ngModel) {
        ngModel.$formatters.push(cents2dollars);
        ngModel.$parsers.push(dollars2cents);
      }
    };
  })
  .filter('dollars2cents', function() { return dollars2cents })
  .filter('cents2dollars', function() { return cents2dollars });

$.urlParam = function(name){
  var result = new RegExp('[\\?&amp;]' + name + '=([^&amp;#]*)').exec(window.location.href);
  return result && result[1] || null;
}

function InvoiceCtrl($scope, $filter) {
  // Product List
  $scope.product_list = [
%  for category in c.product_categories:
%    for product in category.products:
       {
         "id":          ${ product.id },
         "category":    "${ category.name |n }",
         "category_order": ${ category.display_order },
         "product_order": ${ product.display_order },
         "cost":        ${ product.cost },
         "description": "${ product.description |n }",
       },
%    endfor
%  endfor
  ];

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
  $scope.refund.invoice_id = $.urlParam('refund_invoice_id')

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
    $scope.invoice.person_id = $.urlParam('person_id');
  }

  // Processing Status
  $scope.processing = false;

  // Find Person TypeAhead
  $('#person_id').typeahead({
      source: function (query, process) {
          element = this.$element;
          map = {};
          list = [];
          return $.get('/checkin/lookup', { q: query }, function (data) {
              // Only one entry - autoselect it
              if(data.r.length == 1) {
                  entry = data.r[0];

                  map[entry.pretty] = entry.id;

                  // Set the id into the scope
                  $scope.invoice.person_id = entry.id;
                  $scope.$apply()
                  element.blur();
              // Multiple results, provide a list to select from
              } else {
                  $.each(data.r, function(i, entry) {
                      map[entry.pretty] = entry.id;
                      list.push(entry.pretty);
                  });
              }
              return process(list);
          });
      },
      highlighter: function (item) {
          // Only match start of word or line, we don't search mid-string
          var regex = new RegExp( '((?:^|\\s)' + this.query + ')', 'gi' ); 
              return item.replace(regex, "<strong>$1</strong>");
      },
      updater: function (item) {
          $scope.invoice.person_id = map[item];
          return map[item];
      },
  });

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
}
</script>
</head>
  <body ng-controller="InvoiceCtrl">
    <div>
      <h1>New Invoice</h1>
      <label for="person_id" style="display: inline; padding-right: 20px">Person</label><input id="person_id" type="text" ng-model="invoice.person_id" required style="margin: 0;">
      <label for="due_date" style="display: inline; padding-right: 20px">Due Date (dd/mm/yyyy)</label><input id="due_date" type="text" ng-model="invoice.due_date" required style="margin: 0;">
      <br style="margin: 20px"/>
      <table id="invoice_items" class="table table-striped table-bordered">
        <thead>
          <th>Description</th>
          <th>Quantity</th>
          <th>Cost ($, each)</th>
          <th>Product ID</th>
          <th>&nbsp;</th>
        </thead>
        <tbody>
          <tr ng-repeat="item in invoice.items">
            <td>{{ item.description }}</td>
            <td><input type="number" ng-model="item.qty" required></td>
            <td><input type="number" ng-model="item.cost" cents required></td>
            <td>{{ item.product_id }}</td>
            <td style="font-size: 1.2em; margin: 0;"><a ng-click="remove_line($index)">X</a></td>
          </tr>
        </tbody>
        <tbody>
          <tr>
            <td>&nbsp;</td>
            <th align="right" style="text-align: right;">Total</th>
            <td colspan="3">{{ cost_sum() | cents2dollars | currency }}</td>
          </tr>
        </tbody>
      </table>

      <div style="float: right; margin-right: 50px;">
        <a id="new_invoice" class="btn" ng-click="new_invoice($event)" ng-disabled="processing">New Invoice</a>
        <a id="submit_view" class="btn" ng-click="submit_view_invoice($event)" ng-disabled="processing">Save and View</a>
        <a id="submit_new" class="btn" ng-click="submit_new_invoice($event)" ng-disabled="processing">Save and New</a>
        <a id="submit_checkin" class="btn" ng-click="submit_checkin_invoice($event)" ng-disabled="processing">Card</a>
        <a id="submit_pay_checkin" class="btn" ng-click="submit_cash_checkin_invoice($event)" ng-disabled="processing" data-loading-text="Processing">Cash Received</a>
      </div>
    </div>
    <div>
      <h2>Add Product Line</h2>
      <select id="product_select" ng-model="product_select" ng-options="product.description group by product.category for product in product_list | orderBy: ['category_order', 'product_order']" style="width: 400px">
        <option value="">-- Choose Product --</option>
      </select>
      <a id="add_line" class="btn" ng-click="add_line($event)">Add</a>
    </div>
    <div>
      <h2>Add Manual Line</h2>
      <label for="manual_description" style="display: inline; padding-right: 20px">Description:</label><input type="text" id="manual_description" ng-model="manual.description" style="margin: 0;">
      <label for="manual_cost" style="display: inline; padding-right: 20px">Cost $</label><input type="text" id="manual_cost" cents ng-model="manual.cost" style="margin: 0;">
      <a id="add_manual" class="btn" ng-click="add_manual($event)">Add</a>
    </div>
    <div>
      <h2>Refund Existing Invoice</h2>
      <label for="refund_invoice_id" style="display: inline; padding-right: 20px">Invoice ID:</label><input type="number" id=refund_invoice_id" ng-model="refund.invoice_id" style="margin: 0;">
      <a id="refund_invoice" class="btn" ng-click="refund_invoice($event)">Refund Invoice</a>
  </body>
</html>
<!-- vim: set ts=2 sw=2 filetype=html : -->
