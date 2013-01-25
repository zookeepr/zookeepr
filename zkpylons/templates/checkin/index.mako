<!doctype html>
<html ng-app>
	<head>
		<meta charset="utf-8">
		<title>Rego Desk</title>
		<link href="bootstrap/css/bootstrap.min.css" rel="stylesheet" media="screen">
		<script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.0/jquery.min.js"></script>
		<script src="//ajax.googleapis.com/ajax/libs/angularjs/1.0.3/angular.min.js"></script>
		<script src="angular-strap.js"></script>
		<script src="bootstrap/js/bootstrap.js"></script>
		<script type="text/javascript">
			function RegoCtrl($scope) {
				$scope.swag = [
					{
						"title": "Men's Large",
						"quantity": "2",
						"state": "Give out",
					},
					{
						"title": "ANU Parking",
						"quantity": "1",
						"state": "Provided",
					},
				];
				$scope.badge = {
					"status": "Print",
				};
				$scope.identity = {
					"name": "Tristan Goode",
					"ticket": "Miniconf Organiser Ticket",
				};
				$scope.dinners = [
					{"title": "Speakers' Dinner - Adult", "quantity": "2",},
					{"title": "Penguin Dinner - Adult", "quantity": "2",},
				];
				$scope.misc = [
					{ "title": "Partners' Programme - Adult",
						"quantity": "1",
					},
				];
			}

			$(window).load(function(){

				$('#search_box').typeahead({
					local_source: function (query, process) {
						var data = [
							"Andy Jane",
							"Bob Jane",
							"Bob James"
						];
						process (data); // The examples (all) lie.  Don't return this.
					},
					source: function (query, process) { // Next...
						return $.get('/checkin/lookup', { q: query }, function (data) {
							name_lookup = {};
							name_list = [];
							$.each(data.r, function(i, entry) {
								name_lookup[entry.pretty] = entry.id;
								name_list.push(entry.pretty);
							});

							return process(name_list);
						});
					},
					highlighter: function (item) {
						// Only match start of word or line, we don't search mid-string
						var regex = new RegExp( '((?:^|\\s)' + this.query + ')', 'gi' ); 
						return item.replace(regex, "<strong>$1</strong>");
						// return item; // Disable bold highlighting - Better to match work start?
					},
					updater: function (item) {
						console.log("person.id: " + name_lookup[item]);
						return item;
					},
				});
			});
		</script>
		<style type="text/css">
			div {
				margin: 0;
				padding: 0;
			}
			#top_bar {
				position: absolute;
				top: 0;
				left: 0;
				right: 0;
				height: 33px;
				background-color: #7B92D1;
			}
			#body_holder {
				position: absolute;
				top: 33px;
				left: 0px;
				right: 0px;
				bottom: 0px;
			}
			#identity, #stuff, #other, #food {
				width: 45%;
				height: 45%;
				position: absolute;
				border: solid;
				margin: 0;
				padding: 10px;
			}
			#identity {
				top: 0;
				left: 0;
			}
			#stuff {
				top: 0;
				right: 0;
			}
			#other {
				bottom: 0;
				left: 0;
			}
			#food {
				bottom: 0;
				right: 0;
			}
		</style>
	</head>
	<body ng-controller="RegoCtrl">
		<!-- Rego tablets are 800x1232, but can rotate -->
		<div id="top_bar">
			<div style="float: left">
				<table>
					<tr>
						<td>
						</td>
						<td>
						</td>
					</tr>
				</table>
			</div>
			<div style="float: right;">
				<!-- <form class="form-search"> -->
					<input id="search_box" type="text" ng-model="typeaheadValue" bs-typeahead="typeahead" data-items="4" class="span3 input-medium search-query" size="30"/>
					<button type="submit" class="btn">Search</button>
				<!-- </form> -->
			</div>
		</div>

		<div id="body_holder">
			<div id="identity">
				<p style="font-family: 'serif'; font-size: 1.5em; ">
					{{identity.name}}
				</p>
				<p>
					{{identity.ticket}}
				</p>
			</div>
			<div id="stuff">
				<table width="100%">
					<thead>
						<tr>
							<th>Item</th>
							<th align="center">Quantity</th>
							<th align="right">Action</th>
						</tr>
					</thead>
					<tbody>
						<tr>
							<td>Badge</td>
							<td colspan="2" align="right">{{badge.status}}</td>
						</tr>
						<tr ng-repeat="item in swag | orderBy:'name'">
							<td>{{item.title}}</td>
							<td align="center">{{item.quantity}}</td>
							<td align="right">{{item.state}}</td>
						</tr>
					</tbody>
				</table>
			</div>
			<div id="other">
				<table width="100%">
					<thead>
						<tr>
							<th>Item</th>
							<th align="center">Quantity</th>
							<th align="right">Action</th>
						</tr>
					</thead>
					<tbody>
						<tr ng-repeat="stuff in misc | orderBy:'name'">
							<td>{{stuff.title}}</td>
							<td align="center">{{stuff.quantity}}</td>
							<td align="right"></td>
						</tr>
					<tbody>
				</table>
				Notes:
			</div>
			<div id="food">
				<table width="100%">
					<thead>
						<tr>
							<th>Item</th>
							<th align="center">Quantity</th>
							<th align="right">Action</th>
						</tr>
					</thead>
					<tbody>
						<tr ng-repeat="dinner in dinners | orderBy:'name'">
							<td>{{dinner.title}}</td>
							<td align="center">{{dinner.quantity}}</td>
							<td align="right"></td>
						</tr>
					</tbody>
				</table>
			</div>
		</div>
	</body>
</html>
<!-- vim: set ts=2 sw=2: -->
