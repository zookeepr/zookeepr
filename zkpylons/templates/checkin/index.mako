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
            var history = [
                { "id": "10473", "pretty": "Adam Baxter - voltagex@voltagex.org" },
                { "id": "10134", "pretty": "Jacinta Richardson - jarich@perltraining.com.au" },
                { "id": "10702", "pretty": "10702" },
            ];

            var ticket_product_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 55, 80, 81, 84, 87];
            var penguin_dinner_ids = [45, 46, 47];
            var speaker_dinner_ids = [48, 49, 50];
            var partner_program_ids = [52, 53, 54];

            var data = {};

      $.urlParam = function(name){
        var result = new RegExp('[\\?&amp;]' + name + '=([^&amp;#]*)').exec(window.location.href);
        return result && result[1] || null;
      }

            function RegoCtrl($scope) {
                $scope.data = data;
                $scope.block = "";
                $scope.history = history;
                $scope.history_selected = function($event) {
                    id = $event.currentTarget.children[0].innerHTML;
                    pretty = $event.currentTarget.children[1].innerHTML;
                    load_person(id, pretty);
                }
                $scope.swag_action = function($event, id) {
                    console.log(id);
                }
                $scope.badge_action = function($event, fulfilment) {
                    console.log("badge_action", fulfilment);
                    // /fulfilment/fulfilment_id/badge_print
                    $.post('/fulfilment/'+fulfilment.id+'/badge_print', function(print_response) {
                        console.log(print_response);
                        console.log(print_response.status);
                        for (var i = 0; i < data["fulfilments"].length; i++) {
                            var f = data["fulfilments"][i];
                            if(f.id == fulfilment.id) {
                                data["fulfilments"][i]["fulfilment_status"] = print_response.status;
                                $scope.data["fulfilments"][i]["fulfilment_status"] = print_response.status;
                                data["fulfilments"][i]["status_id"] = 6;
                $scope.data["fulfilments"][i]["status_id"] = 6; 
                angular.element(document).scope().$apply(); // Required for history to update too
                angular.element($('body')).scope().$apply();    
                            }
                            $.post('/checkin/update_fulfilments', {data: JSON.stringify(data)}, function(incoming) {
                // Reload all data                              
                load_person(data.id, data.firstname + ' ' + data.lastname); // TODO: Don't want to push to the history                                                   
              });
              // TODO "Loading"   
                            // TODO: Failure
                        }
                    });
                    // TODO "Loading"
                    // TODO Handle failure
                }
                $scope.update_data = function() {
                    console.log("new data", data);
                    for (var i = 0; i < data["fulfilments"].length; i++) {
                        var f = data["fulfilments"][i];
                        if(f.fulfilment_type == 'Badge') {
                            for (var j = 0; j < f["fulfilment_items"].length; j++) {
                                var fi = f["fulfilment_items"][j];
                                if($.inArray(fi.product_id, ticket_product_ids) > -1) {
                                    $scope.ticket = fi.description;
                                }
                                if($.inArray(fi.product_id, penguin_dinner_ids) > -1) {
                                    data["fulfilments"][i]["fulfilment_items"][j].description = "Penguin Dinner " + 
                                        data["fulfilments"][i]["fulfilment_items"][j].description;
                                }
                                if($.inArray(fi.product_id, speaker_dinner_ids) > -1) {
                                    data["fulfilments"][i]["fulfilment_items"][j].description = "Speaker Dinner " + 
                                        data["fulfilments"][i]["fulfilment_items"][j].description;
                                }
                            }
                        }
                        if(f.fulfilment_type == "Partners' Programme") {
                            for (var j = 0; j < f["fulfilment_items"].length; j++) {
                                if($.inArray(fi.product_id, partner_program_ids) > -1) {
                                    data["fulfilments"][i]["fulfilment_items"][j].description = "Partner Programme " + 
                                        data["fulfilments"][i]["fulfilment_items"][j].description;
                                }
                            }
                        }
                    }
                    $scope.data = data;
                    console.log($scope);
                }
                $scope.exclude_ticket = function(elem) { 
                    return ($.inArray(elem.product_id, ticket_product_ids) == -1);
                }
            }

            function load_person(id, pretty) {
                console.log("person.id: " + id + " - " + pretty);
                $('#search_box').val("");
                $("#search_box").focus();

                if(history.push({"id": id, "pretty": pretty}) > 5) {
                    history.shift(); // push returns length, cap max length to 5
                }
                angular.element(document).scope().$apply(); // Required for history to update too

                $.post('/checkin/person_data', { id: id }, function(incoming) {
                    data = incoming;

                    console.log("incoming data", data);
                    for (var i = 0; i < data["notes"].length; i++) {
                        console.log("block", data["notes"][i]);
                        if(data["notes"][i].block) {
                            $("#block_rego_msg").text(data["notes"][i]["note"]);
                            $("#block_rego").modal("show");
                            return; // Don't load new data
                        }
                    }

                    $('#search_box').val("");
                    $("#search_box").focus();
                    angular.element($('body')).scope().update_data();
                    angular.element(document).scope().$apply(); // Required for history to update too
                    angular.element($('body')).scope().$apply();
                });
                // TODO "Loading"
                // TODO Handle failure

            }

            $(window).load(function(){
        console.log($.urlParam('id'));
        if($.urlParam('id')) {
          load_person($.urlParam('id'), "URL");
        }

                $("#search_box").focus();

                $('#search_box').typeahead({
                    source: function (query, process) {
                        return $.get('/checkin/lookup', { q: query }, function (data) {
                            // TODO: length == 0 --> bad stuff
                            if(data.r.length == 1) { // Only one entry - autoselect it
                                load_person(data.r[0].id, data.r[0].pretty);
                                $('#search_box').val(data.r[0].pretty);
                                return process([]);
                            }

                            name_lookup = {};
                            name_list = [];
                            $.each(data.r, function(i, entry) {
                                name_lookup[entry.pretty] = entry.id;
                                name_list.push(entry.pretty);
                            });
                            return process(name_list);
                            // TODO: If there is only one entry - autoselect it
                        });
                    },
                    highlighter: function (item) {
                        // Only match start of word or line, we don't search mid-string
                        var regex = new RegExp( '((?:^|\\s)' + this.query + ')', 'gi' ); 
                        return item.replace(regex, "<strong>$1</strong>");
                    },
                    updater: function (item) {
                        load_person(name_lookup[item], item);
                        return item;
                    },
                });

                $("#stuff_supplied").click(function() {
                    console.log("all stuff supplied");
                    for (var i = 0; i < data["fulfilments"].length; i++) {
                        var f = data["fulfilments"][i];
                        if(f.fulfilment_type == 'Swag') {
                            f.status_id = 3; // Completed
                        }
                    }
                    $.post('/checkin/update_fulfilments', {data: JSON.stringify(data)}, function(incoming) {
                        // Reload all data
                        load_person(data.id, data.firstname + ' ' + data.lastname); // TODO: Don't want to push to the history
                    });
                    // TODO "Loading"
                    // TODO Handle failure
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
                height: 30%;
            }
            #stuff {
                top: 0;
                right: 0;
                height: 95%;
            }
            #other {
                bottom: 0;
                left: 0;
                height: 30%;
            }
            #food {
                bottom: 33%;
                left: 0;
                height: 30%;
            }
            #stuff_supplied {
                height: 80px;
                width: 300px;

                /* Colour green with darker green border */
                background-color: #00B000;
                background-image: none; /* Disable default gray gradient */
                border: solid;
                border-color: #008000;

                /* Strengthen the text so it still looks ok */
                font-size: 1.2em;
                font-weight: bolder;

                box-shadow: 3px 3px 5px 6px;

                position: absolute;
                left: 50%;
                margin-left: -150px; /* width/2 */
                bottom: 20px;
            }
            #history_list {
                width: 400px;
            }
            #history_btn {
                width: 400px;
                text-align: right;
            }
            .notes {
                margin-left: 20px;
            }
        </style>
    </head>
    <body ng-controller="RegoCtrl">
        <!-- Rego tablets are 800x1232, but can rotate -->
        <div id="block_rego" class="modal hide fade" style="display: none; width: 50%; height: 50%;">
            <h1 style="text-align: center;">Registration Blocked</h1>
            <p id="block_rego_msg" style="margin-left: 20px; margin-top: 4em; font-size: 2em;">
            </p>
            <a onclick='$("#block_rego").modal("hide")' class="btn" style="position: absolute; right: 20px; bottom: 20px;">Close</a>
        </div>
        <div id="top_bar">
            <div style="float: left; margin-left: 5px; margin-right: 100px;">
                <a id="new_invoice" ng-click="new_invoice()" class="btn" href="/invoice/new?id={{data.id}}">New Invoice</a>
            </div>
            <div style="float: left;" class="dropdown">
                <a id="history_btn" role="button" class="dropdown-toggle btn" data-toggle="dropdown" href="#">History<b class="caret"></b></a>
                <ul id="history_list" class="dropdown-menu" role="menu" aria-labelledby="history_btn">
                    <li ng-repeat="h in history" ng-click=history_selected($event)>
                        <span style="display: none">{{h.id}}</span>
                        <span>{{h.pretty}}</span>
                    </li>
                </ul>
            </div>
            <div style="float: right;">
                <input id="search_box" type="text" ng-model="typeaheadValue" bs-typeahead="typeahead" data-items="4" class="span3 input-medium search-query" placeholder="Search" size="30"/>
            </div>
        </div>

        <div id="body_holder">
            <div id="identity">
                <p style="font-family: 'serif'; font-size: 1.5em; ">
                    {{data.firstname}} {{data.lastname}}
                </p>
                <p>
                    {{data.email_address}}
                </p>
                <p>
                    {{ticket}}
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
                        <tr ng-repeat="fulfilment in data.fulfilments | filter:{'fulfilment_type':'Badge'}">
                            <td>Badge</td>
                            <td colspan="2" align="right"><a ng-click="badge_action($event, fulfilment)">{{fulfilment.fulfilment_status}}</a></td>
                        </tr>
                        <!-- TODO: Link badges to fulfilments -->
                    </tbody>
                    <tbody>
                        <tr><td colspan="3">&nbsp;</td></tr> <!-- white space -->
                    </tbody>
                    <tbody ng-repeat="fulfilment in data.fulfilments | filter:{'fulfilment_type':'Swag'}">
                        <tr ng-repeat="item in fulfilment.fulfilment_items | orderBy:'description'">
                            <td>{{item.description}}</td>
                            <td align="center">{{item.qty}}</td>
                            <td align="right"><a ng-click="swag_action($event, item)">{{fulfilment.fulfilment_status}}</a></td>
                        </tr>
                    </tbody>
                </table>
                <button id="stuff_supplied" type="submit" class="btn">All Supplied</button>
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
                    <tbody ng-repeat="fulfilment in data.fulfilments | filter:{'fulfilment_type':'Accommodation'}">
                        <tr ng-repeat="item in fulfilment.fulfilment_items | orderBy:'description'"> 
                            <td>{{item.description}}</td>
                            <td align="center">{{item.qty}}</td>
                            <td align="right">{{fulfilment.fulfilment_status}}</td>
                        </tr>
                    </tbody>
                    <tbody ng-repeat="fulfilment in data.fulfilments | filter:{'fulfilment_type':'Partners\' Programme'}">
                        <tr ng-repeat="item in fulfilment.fulfilment_items | orderBy:'description'"> 
                            <td>{{item.description}}</td>
                            <td align="center">{{item.qty}}</td>
                            <td align="right">{{fulfilment.fulfilment_status}}</td>
                        </tr>
                    </tbody>
                </table>
                Notes:
                <p class="notes" ng-repeat="note in data.notes | orderBy:id">
                    {{note.note}}
                </p>
            </div>
            <!-- TODO: Filter out old stuff -->
            <div id="food">
                <table width="100%">
                    <thead>
                        <tr>
                            <th>Item</th>
                            <th align="center">Quantity</th>
                            <th align="right">Action</th>
                        </tr>
                    </thead>
                    <tbody ng-repeat="fulfilment in data.fulfilments | filter:{'fulfilment_type':'Badge'}">
                        <tr ng-repeat="item in fulfilment.fulfilment_items | filter:exclude_ticket | orderBy:'description'"> 
                            <td>{{item.description}}</td>
                            <td align="center">{{item.qty}}</td>
                            <td align="right">{{fulfilment.fulfilment_status}}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </body>
</html>
<!-- vim: set ts=2 sw=2: -->
