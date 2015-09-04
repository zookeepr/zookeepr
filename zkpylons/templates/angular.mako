<%def name="title()">${ c.config.get("event_byline") }</%def>
<%def name="extra_head()"></%def>
<%def name="short_title()"></%def>
<%def name="toolbox_extra()"></%def>
<%def name="toolbox_extra_admin()"></%def>
<%def name="toolbox_extra_reviewer()"></%def>
<%def name="toolbox_extra_funding_reviewer()"></%def>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html lang="en-us">
	<head>
	  <meta charset="utf-8">
		<title>${ self.title() }</title>
		<base href="/">
		<link rel="prefetch" href="https://login.persona.org/include.js">
		<link rel="shortcut icon" href="/images/favicon.ico" type="image/x-icon">
		<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css">
		<link rel="stylesheet" media="screen, projection" href="/screen.css" type="text/css" />
		<link rel="stylesheet" media="screen" href="/css/lightbox.css" type="text/css" />
		<link rel="stylesheet" media="print" href="/print.css" type="text/css" />
		<link href="/media/news/rss" rel="alternate" type="application/rss+xml" title="LCA2011 News">

		${self.extra_head()}

		<!-- For production: <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.1.17/require.min.js" data-main="angular/routing.js"></script> -->
		<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.1.17/require.js" data-main="angular/routing.js" async></script>

	</head>
<body>
	<div id="wrapper">
		<div id="head">
			<div id="page-logo"> <img src="/images/logo.png"> </div>
			<div></div>
			<div id="page-title">${ c.config.get('event_name') }</div>
			<div id="page-subtitle">A ${ c.config.get('event_parent_organisation') } Conference</div>
		</div>
		<div id="columns">
			<div id="col-left">
				<div id="sidebar">
					<h3>Toolbox</h3>      <%include file="/leftcol/toolbox.mako" args="parent=self" />
					<h3>News</h3>         <%include file="/leftcol/news.mako" />
					<h3>In the press</h3> <%include file="/leftcol/in_the_press.mako" />
				</div>
			</div><!-- col-left -->

			<div id="col-right">
				<div id="navigation">
					<%include file="/nav.mako" />
					<%include file="/subnav.mako" />
					<%include file="/subsubnav.mako" />
				</div>
				<div id="content">
					<dynamic-include controller="loaded_ctrl" include="request + '.html'">
				</div>
				<div id="footer">© 2011 Zookeepr</div>
			</div><!-- col-right -->
		</div><!-- columns -->
	</div>
</body>
</html>
