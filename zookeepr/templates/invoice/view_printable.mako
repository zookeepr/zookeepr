<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html lang="en-us">
<head>
<title>Tax Invoice/Statement - ${ h.lca_info['event_name'] }</title>
<link rel="icon" type="image/png" href="/images/favicon.ico">
</head>
<body>

<%include file="view_fragment.mako" />

  </body>
</html>

<%def name="title()">
Tax Invoice/Statement - ${ caller.title() }
</%def>
