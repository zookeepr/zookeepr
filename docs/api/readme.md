# API README


## Table of Contents

 * [Summary](#summary)
 * [Methods](#methods)
 * [Versioning](#versioning)
 * [Collection](#collection)
 * [Headers](#headers)
 * [Status Code](#status-code)
 * [Response](#response)
 * [Error handling](#error-handling)

## Summary

API will be accessed using the following pattern of the URLs:


Method | URL                            | Description
------ | ------------------------------ | -----------------------
GET    | /api/v1.0/                     | Lists available collections
GET    | /api/v1.0/items/               | Gets all members of items
GET    | /api/v1.0/items/12             | Gets item 12
POST   | /api/v1.0/items/               | Create a new item
PUT    | /api/v1.0/items/12             | Replace item 12
PATCH  | /api/v1.0/items/12             | Change a portion of item 12
DELETE | /api/v1.0/items/12             | Delete item 12
GET    | /api/v1.0/items/12/more_items/ | Gets all members of more_items in item 12

All data will be exchanged in JSON format.

The API will adopt REST principles where appropriate, HATEOAS discoverability is not required.

When designing an API the existing APIs should be reviewed to ensure consistency.
As new APIs are developed and the structure is refined this document should also be updated.


## Methods

The API supports client requests using a subset of these HTTP methods.

Method  | Description
------- | -----------
GET     | Retrieve records.
HEAD    | Retrieve record metadata.
POST    | Create a new record.
PUT     | Replace an existing record with a new record.
PATCH   | Update a portion of an existing record.
DELETE  | Remove a record.


## Versioning

A good REST API should be versioned.  However, the API will evolve rather than be designed up front, this requires some compromises. So versioning will be handled with the following rules:

1. The start version is 1.0
2. A minor version bump will be performed for minor backwards incompatible changes, such as changing a rarely used field.
3. A major version bump will occur for a major backwards incompatible change, such as removing or restructuring a data collection.
4. Versioning bumps will only occur due to changes in publicly usable api areas.

This means that we can add additional API collections without constantly incrementing the version numbers but still provide consistency for API consumers.


## Collection

The data is grouped into collections, each collection is designated with a plural noun.

Each collection is documented at `/docs/api/<collection name>.md`

All data in a collection can be accessed at `/api/<version>/<collection name>`

Individual members of a collection can be accessed at `/api/<version>/<collection name>/<identifier>`

If an item links to other data it can be brought it at `/api/<version/<collection name>/<identifier>/<further collection>`

Each collection is tested by test scripts at /zkpylons/tests/api/<collection name>/

## Headers

Collection metadata should be placed in header fields.

Pagination should be done with the RFC5988 link header, 

Caching should be performed using both the ETag and Last-Modified headers.

Data retrieval operations should support the If-Modified-Since and If-None-Match headers.

Data modification operations should support the If-Unmodified-Since and If-Match headers.


## Status Code

The API returns a subset of these HTTP status codes.

Code | Code Text             | Description
---- | --------------------- | -----------
200  | OK                    | Default return, indicates a successful request.
201  | Created               | Used to indicate a successful record created from a POST request.
204  | No Content            | Used to indicate a successful PUT, PATCH or DELETE operation.
304  | Not Modified          | Used when retrieving data which fails the If-Modified-Since or If-None-Match headers
400  | Bad Request           | Used to report badly formatted request payloads.
401  | Unauthorized          | Used when the user has insufficient permissions for the operation.
404  | Not Found             | Used when a requested item or collection does not exist.
405  | Method Not Allowed    | Used when a method which is invalid for the given URL is used.
412  | Precondition Failed   | Used when modifying data which fails the If-Unmodified-Since or If-Match headers.
500  | Internal Server Error | Used for a server error such as database failure.


## Response

The response must be JSON formatted, the top level is an array or object as appropriate.

An empty response is also permitted when it is appropriate and specifically documented.


## Error handling

In the event of an error an appropriate status code should be returned in addition to a JSON object corresponding to the following format.

	{'message': <message detail> [, <optional extra error specific detail>]}

Internal server errors must also be logged at the error level.

