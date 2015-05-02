Registration Management
-----------------------

Background on how the Rego process works on the Rego desk

Key areas regarding fullfillment are
 * Swag
 * Badge
 * Accommodation
 * Partner Program

Tablet friendly Rego Interface can be found at 
 * http://zookeepr:6543/admin/#/checkin

SWAG
----
This includes
 * Bag
 * T-Shirt

Badge
-----
This has its own fullfilment type and is usually printed on-demand at Rego Desk.

Before Rego starts all Badges marked "Give Out" need to be changed to "Print"

Ideally change the default fulfilment_type of Badge to Print via 
 - https://linux.conf.au/fulfilment_type

Otherwise id can be fixed in the database after running https://linux.conf.au/admin/generate_fulfilment

 - SELECT * from fulfilment where type_id=2 and status_id=1;

 - UPDATE fulfilment set status_id=10 where type_id=2 and status_id=1;

Badge currently doesn''t reflect Child tickets for the Events

