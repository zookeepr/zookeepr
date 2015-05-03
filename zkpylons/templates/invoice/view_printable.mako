<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html lang="en-us">
<head>
<title>Tax Invoice/Statement - ${ c.config.get('event_name') }</title>
<link rel="icon" type="image/png" href="/images/favicon.ico">
<style type="text/css">
 .invoice_invalid {
	background: url('/invalid.png');
}
</style>
</head>
<body>

<%include file="view_fragment.mako" />

  </body>
</html>

<%def name="title()">
Tax Invoice/Statement - ${ parent.title() }
</%def>
