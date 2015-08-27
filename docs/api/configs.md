# Configs API


## Table of Contents

 * [Introduction](#introduction)
 * [GET /api/v1.0/configs/](#get-apiv10configs)
 * [GET /api/v1.0/configs/:category](#get-apiv10configscategory)
 * [GET /api/v1.0/configs/:category/:key](#get-apiv10configscategorykey)
 * [PUT /api/v1.0/configs/:category/:key](#put-apiv10configscategorykey)

## Introduction

This API allows the retrieval and updating of site config values such as the event name, contact email address or payment gateway details.

Due to the sensitivity of some of the configuration values this API is only accessible by site administrators.

It is not possible to delete or create new config variables using this API. These variable are tied into site functionality so their creation or removal should be part of the commit that changes the related functionality.


## GET /api/v1.0/configs/

Get all config values.

### Authentication

Admin role required

### Request parameters

None supported

### Request headers

Header            | Behaviour
----------------- | ---------
If-Modified-Since | Returns 304 status with empty body if data is unmodified
If-None-Match     | Returns 304 status with empty body if data matches the ETag

### Response headers

Header        | Content
------------- | -------
Content-Type  | application/json; charset=utf-8
Cache-Control | private, max-age=600
Last-Modified | RFC 1123 timestamp of the most recently modified entry
ETag          | Server defined hash

### Response data

	[
		{
			category: <category string>,
			key: <key string>,
			value: <value string or complex JSON data>,
			description: <description string>
		},
		...
	]

### Error handling

Specifying a non-existent category and key pair will result in a 404 status.

A non-admin use will get a 401 status. The error message will specify that admin rights are required.

An internal processing error, such as a failure to communicate with the database will cause the return of a 500 status. The response data shall include an error message.


## GET /api/v1.0/configs/:category

Get all config values for a specific category.

### Authentication

Admin role required

### Request parameters

None supported

### Request headers

Header            | Behaviour
----------------- | ---------
If-Modified-Since | Returns 304 status with empty body if data is unmodified
If-None-Match     | Returns 304 status with empty body if data matches the ETag

### Response headers

Header        | Content
------------- | -------
Content-Type  | application/json; charset=utf-8
Cache-Control | private, max-age=600
Last-Modified | RFC 1123 timestamp of the most recently modified entry
ETag          | Server defined hash

### Response data

	[
		{
			category: <category string>,
			key: <key string>,
			value: <value string or complex JSON data>,
			description: <description string>
		},
		...
	]


### Error handling

Specifying a non-existent category and key pair will result in a 404 status.

A non-admin use will get a 401 status. The error message will specify that admin rights are required.

An internal processing error, such as a failure to communicate with the database will cause the return of a 500 status. The response data shall include an error message.


## GET /api/v1.0/configs/:category/:key

Get a specific config value.

### Authentication

Admin role required

### Request parameters

None supported

### Request headers

Header            | Behaviour
----------------- | ---------
If-Modified-Since | Returns 304 status with empty body if data is unmodified
If-None-Match     | Returns 304 status with empty body if data matches the ETag

### Response headers

Header        | Content
------------- | -------
Content-Type  | application/json; charset=utf-8
Cache-Control | private, max-age=600
Last-Modified | RFC 1123 timestamp
ETag          | Server defined hash

### Response data

	{
		category: <category string>,
		key: <key string>,
		value: <value string or complex JSON data>,
		description: <description string>
	}

### Error handling

Specifying a non-existent category and key pair will result in a 404 status.

A non-admin use will get a 401 status. The error message will specify that admin rights are required.

An internal processing error, such as a failure to communicate with the database will cause the return of a 500 status. The response data shall include an error message.


## PUT /api/v1.0/configs/:category/:key

Update a specific config value.

### Authentication

Admin role required

### Request parameters

None supported

### Request headers

Header              | Behaviour
------------------- | ---------
If-Unmodified-Since | Returns 412 status with empty body if data has been modified
If-Match            | Returns 412 status with empty body if data doesn't match the ETag

### Request body

	{
		value: <value string or complex JSON data>
	}

### Response headers

If the update was successful a 204 No Content status is returned.

Unsuccessful updates are discussed in the error handling section.

### Response headers

Header        | Content
------------- | -------
Content-Type  | application/json; charset=utf-8
Cache-Control | no-cache
Last-Modified | RFC 1123 timestamp of the new entry
ETag          | Server defined hash, matches a GET of the new entry

### Response data

Empty, no content sent.

### Error handling

Specifying a non-existent category and key pair will result in a 404 status.

A non-admin use will get a 401 status. The error message will specify that admin rights are required.

Specifying a request body which is not in the correct format, such as malformed JSON or including extra fields, will result in a 400 status. The response data may include an error message.

An internal processing error, such as a failure to communicate with the database will cause the return of a 500 status. The response data shall include an error message.
