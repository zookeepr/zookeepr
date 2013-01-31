<!doctype html>
<html ng-app="invoice">
<head>
<title>Create Invoice</title>
<script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js"></script>
<script src="//ajax.googleapis.com/ajax/libs/angularjs/1.0.3/angular.min.js"></script>
<script src="/bootstrap/js/bootstrap.js"></script>
<link href="/bootstrap/css/bootstrap.min.css" rel="stylesheet" media="screen">


<script type="text/javascript">
var product_list = [
%  for category in c.product_categories:
%   if category.name == 'Swag':
%    for product in category.products:
       {
         "id":          "${ product.id }",
         "cost":        "${ product.cost }",
         "description": "${ product.description }",
         "category":    "${ category.name }",
         "qty":         "1",
       },
%    endfor
%   endif
%  endfor
];

angular.module('invoice', [])
  .directive('cents', function() {
    return {
      // restrict: 'A',
      require: 'ngModel',
      link: function(scope, element, attr, ngModel) {
        function cents2dollars(text) {
          return (text || 0)*100;
        }
        function dollars2cents(text) {
          return (text || 0)/100;
        }
        // ngModel.$parsers.push(dollars2cents);
        // ngModel.$formatters.push(cents2dollars);
        ngModel.$parsers.push(cents2dollars);
        ngModel.$formatters.push(dollars2cents);
      }
    };
  });

$.urlParam = function(name){
  var result = new RegExp('[\\?&amp;]' + name + '=([^&amp;#]*)').exec(window.location.href);
  return result && result[1] || null;
}

function InvoiceCtrl($scope) {
  $scope.product_list = product_list;
  $scope.lines = [];
  $scope.new_product = null;
  $scope.manual_dialog = false;
  console.log($.urlParam('id'));
  $scope.person_id = $.urlParam('id');

  var today = new Date();
  var dd = today.getDate();
  var mm = today.getMonth()+1; //January is 0!
  var yyyy = today.getFullYear();
  if (dd<10) {dd='0'+dd}
  if (mm<10) {mm='0'+mm}
  $scope.due_date = dd+'/'+mm+'/'+yyyy;

  $scope.add_entry = function($event) {
    console.log("new_product", $scope.new_product);
    if($scope.new_product != null) {
      $scope.lines.push($scope.new_product);
    }
  };
  $scope.delete_entry = function(line) {
    console.log("delete_entry", line);
    $scope.lines = jQuery.grep($scope.lines, function(l) {
      return line.id != l.id
    });
  };
  $scope._prep_invoice = function() {
    var invoice = {
      person_id:     $scope.person_id,
      due_date:      $scope.due_date,
      invoice_items: [], // $scope.lines,
    };
    $.each($scope.lines, function(i, v) {
      invoice.invoice_items.push({product_id: v.id, cost: v.cost, qty: v.qty});
    });

    console.log("invoice_out", invoice);
    return invoice;
  }

  $scope.processing = false;

  $scope.submit_invoice = function($event) {
    if($scope.processing) {
      $event.preventDefault();
      return false;
    } else {
      $scope.processing = true;
      $("#submit_cc").addClass('disabled');
      $("#submit_cash").addClass('disabled');
      $("#submit_cc").text('Processing');
    }

    invoice = $scope._prep_invoice();

    $.post('/invoice/save_new_invoice', {invoice: JSON.stringify(invoice)}, function(response) {
      // Response in an invoice id
      console.log("response", response);
      // They have to pay by card... all done
      window.location.href = '/checkin?id=' + $scope.person_id;
    });
  };

  $scope.submit_cash_invoice = function($event) {
    if($scope.processing) {
      $event.preventDefault();
      return false;
    } else {
      $scope.processing = true;
      $("#submit_cc").addClass('disabled');
      $("#submit_cash").addClass('disabled');
      $("#submit_cash").text('Processing');
    }

    invoice = $scope._prep_invoice();

    $.post('/invoice/save_new_invoice', {invoice: JSON.stringify(invoice)}, function(response) {
      // Response in an invoice id
      console.log("response", response);

      // They have paid cash, submit payment
      $.post('/invoice/pay_invoice', {invoice: response}, function(response) {
        console.log("response", response);

        // Now we need to regenerate the invoices
        $.get('/admin/generate_fulfilment', function(response) {
          // Finally all done
          window.location.href = '/checkin?id=' + $scope.person_id;
        });
      });

    });
  };

  $scope.cost_sum = function() {
    var sum = 0;
    $.each($scope.lines, function(i,v) {
      sum += parseInt(v.cost);
    });
    return sum/100; // cents -> dollars
  };
}
</script>
</head>
<body ng-controller="InvoiceCtrl">
<div>
<h1>New Invoice</h1>

<label for="person_id" style="display: inline; padding-right: 20px">Person ID</label><input id="person_id" type="text" ng-model="person_id" style="margin: 0;">
<label for="due_date" style="display: inline; padding-right: 20px">Due Date (dd/mm/yyyy)</label><input id="due_date" type="text" ng-model="due_date" style="margin: 0;">
<br style="margin: 20px"/>
<!-- TODO: Is Due date required? -->

<table id="invoice_entries" class="table table-striped table-bordered">
  <thead>
    <th>Description</th>
    <th>Quantity</th>
    <th>Cost ($, each)</th>
    <th>&nbsp;</th>
  </thead>
  <tbody>
    <tr ng-repeat="line in lines">
      <td>{{line.description}}</td>
      <td><input type="text" ng-model="line.qty"></td>
      <td><input type="text" cents ng-model="line.cost"></td>
      <td style="font-size: 1.2em; margin: 0;"><a ng-click="delete_entry(line)">X</a></td>
    </tr>
  </tbody>
  <tbody>
    <tr>
      <td>&nbsp;</td>
      <th align="right" style="text-align: right;">Total</th>
      <td colspan="2">$ {{ cost_sum() }}</td>
    </tr>
  </tbody>
</table>

<select id="add_entry_select" ng-model="new_product" ng-options="product.description group by product.category for product in product_list" style="width: 400px">
<option>--</option>
</select>
<a id="add_entry" class="btn" ng-click="add_entry($event)">Add</a>
<!-- TODO: <a class="btn" ng-click="manual_dialog=true">Add Manual</a> -->

</div>

<div style="float: right; margin-right: 50px;">
<a id="submit_cc" class="btn" ng-click="submit_invoice($event)">Pay Card</a>
<a id="submit_cash" class="btn" ng-click="submit_cash_invoice($event)" data-loading-text="Processing">Pay Cash</a>
</div>

</body>
</html>

<!-- vim: set ts=2 sw=2 filetype=html : -->
