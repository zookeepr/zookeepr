<%def name="title()">${ c.config.get("event_byline") }</%def>
## Defines required to stop mako from breaking, many are not utilised
<%def name="extra_head()"></%def>
<%def name="extra_body()"></%def>
<%def name="short_title()"></%def>
<%def name="big_promotion()"></%def>
<%def name="toolbox_extra()"></%def>
<%def name="toolbox_extra_admin()"></%def>
<%def name="toolbox_extra_reviewer()"></%def>
<%def name="toolbox_extra_funding_reviewer()"></%def>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html lang="en-us">
	<head>
		<meta charset="utf-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<title>${ self.title() }</title>
		<base href="/">
		<link rel="icon" type="image/x-icon" href="/favicon.ico">

		<link rel="stylesheet" href="/css/bootstrap.css">
		<!-- Custom styles for this template -->
		<link href="/css/carousel.css" rel="stylesheet">
		<link href="/css/simple-sidebar.css" rel="stylesheet">

		<!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
		<!--[if lt IE 9]>
		<script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
		<script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
		<![endif]-->

		${self.extra_head()}

		<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.1.17/require.min.js" data-main="angular/routing.js" async></script>

	</head>

<body>
	<!-- Top menu bar -->
	<div class="navbar-wrapper">
		<div class="container">
			<nav class="navbar navbar-inverse navbar-static-top">
				<div class="container">
					<div class="navbar-header">
						<button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
							<span class="sr-only">Toggle navigation</span>
							<span class="icon-bar"></span>
							<span class="icon-bar"></span>
							<span class="icon-bar"></span>
						</button>
						<a class="navbar-brand" href="#">${ c.config.get('event_name') }</a>
					</div>
					<%include file="nav.mako" />
				</div>
			</nav>
		</div>
    </div>

	<%include file="/leftcol/banner.mako" />


	<div id="wrapper">
		<!-- Sidebar -->
		<div id="sidebar-wrapper">
			<div id="background-image-disabled"></div>
			<ul class="sidebar-nav">
				<%include file="/leftcol/toolbox.mako" args="parent=self" />
			</ul>
		</div>

		<!-- Wrap the rest of the page in another container to center all the content. -->
		<div id="page-content-wrapper" class="toggled">
			<a href="#menu-toggle" class="btn btn-default btn-xs" id="menu-toggle" style="margin-left: -13px;">Toggle Menu</a>
    
			<div class="container-fluid">
				<div class="col-md-8 col-md-offset-2">
					<%include file="/flash.mako" />
					<dynamic-include controller="loaded_ctrl" include="request + '.html'">
				</div>

				<footer class="col-md-8 col-md-offset-2">
					<p style="text-align: center;">&copy; 2015 linux.conf.au 2016 and <a href="http://linux.org.au">Linux Australia</a> &middot; Linux is a registered trademark of Linus Torvalds &middot; <a href="/sitemap">Sitemap</a></p>
					<p class="pull-right"><a href="#">Back to top</a></p>
				</footer>
			</div>

		</div><!-- /.container page-content-wrapping-->
	</div><!--/.container wrapper -->


    <!-- Bootstrap core JavaScript
    ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
    <script src="/js/bootstrap.min.js"></script>
    <script src="/js/validator.min.js"></script>
    <script src="/js/sorttable.js"></script>
    <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
    <script src="/js/ie10-viewport-bug-workaround.js"></script>
    
    <!-- Sidebar Menu Toggle Script -->
    <script>
    $("#menu-toggle").click(function(e) {
        e.preventDefault();
        $("#wrapper").toggleClass("toggled");
    });
    </script>
    <script>
      (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
      (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
      m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
      })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

      ga('create', 'UA-63600300-1', 'auto');
      ga('send', 'pageview');

    </script>
  </body>
</html>

