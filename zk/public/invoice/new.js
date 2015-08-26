define(['angular', 'cents'], function(angular, cents) {
	var module_name = 'new';
	angular.module(module_name, [cents]).controller(module_name, new_ctrl);
	new_ctrl.$inject = ['$scope', '$http', '$filter'];
	return module_name;
});

function get_urlParam(name) {
	var result = new RegExp('[\\?&amp;]' + name + '=([^&amp;#]*)').exec(window.location.href);
	return result && result[1] || null;
}

function new_ctrl($scope, $http, $filter) {
	// Product List
	$scope.product_list = [];
	$http.get('/invoice/product_list').then(function(response) {
		if(response.status != 200)
			throw new Error("Could not fetch product_list");

		var data = response.data;
		data.forEach(function(category) {
			category.products.forEach(function(product) {
				$scope.product_list.push({
					"id" :             product.id,
					"category" :       category.name,
					"category_order" : category.display_order,
					"product_order" :  product.display_order,
					"cost" :           product.cost,
					"description" :    product.description,
				});
			});
		});
	});

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
		});
	};

	// Refund Schema
	$scope.refund = {};
	$scope.refund.invoice_id = get_urlParam('refund_invoice_id')

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
			}
			$scope.get_invoice($event, callback, $scope.refund.invoice_id);
		}
	};

	$scope.get_invoice = function($event, callback, invoice_id) {
		$.get(invoice_id + '/get_invoice', callback);
	};

	// Check if we have been given a refund to process
	if ($scope.refund.invoice_id) {
		$scope.new_invoice();
		$scope.refund_invoice();
	// Otherwise create a new empty invoice
	} else {
		$scope.new_invoice();
		$scope.invoice.person_id = get_urlParam('person_id');
	}

	// Processing Status
	$scope.processing = false;

	// Find Person TypeAhead
	/* -- Was using Bootstrap 2 typeahead, dropped in BS 3
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
	*/

	$scope.cost_sum = function() {
		var sum = 0;
		$.each(
			$scope.invoice.items, function(i,v) {
				sum += (parseInt(v.qty) || 0) * (parseInt(v.cost) || 0);
			}
		);
		return sum
	};

	$scope.add_line = function() {
		console.log("Add line", $scope, $scope.product_select);
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
			window.location.href = response['r']['invoice_id'];
		};
		return $scope.submit_invoice($event, callback)
	}

	$scope.submit_new_invoice = function($event) {
		callback = function(response) {
			$scope.processing = false;
			// Response in an invoice id
			$scope.new_invoice();
		};
		return $scope.submit_invoice($event, callback)
	}

	$scope.submit_checkin_invoice = function($event) {
		callback = function(response) {
			$scope.processing = false;
			// Response in an invoice id
			// They have to pay by card... all done
			window.location.href = '/admin/#/checkin?id=' + $scope.invoice.person_id;
		};
		return $scope.submit_invoice($event, callback)
	};

	$scope.submit_cash_checkin_invoice = function($event) {
		callback = function(response) {
			$scope.processing = false;
			// Response is an invoice id
			callback = function(response) {
				$scope.processing = false;
				window.location.href = '/admin/#/checkin?id=' + $scope.invoice.person_id;
			};
			return $scope.submit_payment($event, callback, response['r']['invoice_id']);
		};
		return $scope.submit_invoice($event, callback)
	};
}
