<%def name="title()">${ c.config.get("event_byline") }</%def>
<%def name="short_title()">
   ## Defined in children
</%def>
<%def name="extra_head()">
    ## Defined in children
</%def>
<%def name="extra_body()">
  <body>
</%def>
<%def name="big_promotion()">
    ## Defined in children
</%def>
<%def name="toolbox_extra()">
    ## Defined in children
</%def>
<%def name="toolbox_extra_admin()">
    ## Defined in children
</%def>
<%def name="toolbox_extra_reviewer()">
    ## Defined in children
</%def>
<%def name="toolbox_extra_funding_reviewer()">
    ## Defined in children
</%def>
<%def name="contents()">
    ## Defined in children
</%def>
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
    <meta name="description" content="">
    <meta name="author" content="">
    <link rel="icon" type="image/x-icon" href="/favicon.ico">

    <title>${ self.title() }</title>

    <!-- Bootstrap core CSS -->
    <link href="/css/bootstrap.css" rel="stylesheet">
    <!-- Custom styles for this template -->
    <link href="/css/carousel.css" rel="stylesheet">
    <link href="/css/simple-sidebar.css" rel="stylesheet">

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!--[if lt IE 9]>
      <script src="https://oss.maxcdn.com/html5shiv/3.7.2/html5shiv.min.js"></script>
      <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->
  </head>
<!-- NAVBAR
================================================== -->
  <body>
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
            <div id="navbar" class="navbar-collapse collapse">
<!-- This was the original nav bar code
              <ul class="nav navbar-nav">
                <li class="active"><a href="#">Home</a></li>
                <li><a href="#about">About</a></li>
                <li><a href="#contact">Contact</a></li>
                <li class="dropdown">
                  <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="false">Dropdown <span class="caret"></span></a>
                  <ul class="dropdown-menu" role="menu">
                    <li><a href="#">Action</a></li>
                    <li><a href="#">Another action</a></li>
                    <li><a href="#">Something else here</a></li>
                    <li class="divider"></li>
                    <li class="dropdown-header">Nav header</li>
                    <li><a href="#">Separated link</a></li>
                    <li><a href="#">One more separated link</a></li>
                  </ul>
                </li>
              </ul>
-->
            </div>
          </div>
        </nav>
      </div>
    </div>


    <!-- Carousel
    ================================================== -->
      <%include file="/leftcol/banner.mako" />
    <!-- /.carousel -->

  <div id="wrapper"><!-- Main wrapper for the sidebar -->
    <!-- Sidebar -->
        <div id="sidebar-wrapper">
            <div id="background-image-disabled"></div>
            <ul class="sidebar-nav">
                <%include file="/leftcol/toolbox.mako" args="parent=self" />
            </ul>
        </div>
    <!-- /#sidebar-wrapper -->

    <!-- Marketing messaging and featurettes
    ================================================== -->
    <!-- Wrap the rest of the page in another container to center all the content. -->
    <div id="page-content-wrapper" class="toggled">
    <a href="#menu-toggle" class="btn btn-default btn-xs" id="menu-toggle" style="margin-left: -13px;">Toggle Menu</a>
    
    <div class="container-fluid marketing">
    <!-- START THE FEATURETTES -->
      <div class="row featurette">
        <div class="col-md-8 col-md-offset-2">
          <%include file="/flash.mako" />
          ${next.body()}
        </div>
       <div class="col-md-8 col-md-offset-2">
          <br />
          <img class="featurette-image img-responsive center-block" src="/img/Geelong-Wave-Gradient-greyscale-small.png" alt="Geelong 2016">
        </div>
      </div>
<%doc>
      <div class="row featurette">
        <div class="col-md-7">
          <h2 class="featurette-heading">First featurette heading. <span class="text-muted">It'll blow your mind.</span></h2>
          <p class="lead">Donec ullamcorper nulla non metus auctor fringilla. Vestibulum id ligula porta felis euismod semper. Praesent commodo cursus magna, vel scelerisque nisl consectetur. Fusce dapibus, tellus ac cursus commodo.</p>
        </div>
      </div>

      <hr class="featurette-divider">

      <div class="row featurette">
        <div class="col-md-7 col-md-push-5">
          <h2 class="featurette-heading">Oh yeah, it's that good. <span class="text-muted">See for yourself.</span></h2>
          <p class="lead">Donec ullamcorper nulla non metus auctor fringilla. Vestibulum id ligula porta felis euismod semper. Praesent commodo cursus magna, vel scelerisque nisl consectetur. Fusce dapibus, tellus ac cursus commodo.</p>
        </div>
        <div class="col-md-5 col-md-pull-7">
          <img class="featurette-image img-responsive center-block" data-src="holder.js/500x500/auto" alt="Generic placeholder image">
        </div>
      </div>

      <hr class="featurette-divider">

      <div class="row featurette">
        <div class="col-md-7">
          <h2 class="featurette-heading">And lastly, this one. <span class="text-muted">Checkmate.</span></h2>
          <p class="lead">Donec ullamcorper nulla non metus auctor fringilla. Vestibulum id ligula porta felis euismod semper. Praesent commodo cursus magna, vel scelerisque nisl consectetur. Fusce dapibus, tellus ac cursus commodo.</p>
        </div>
        <div class="col-md-5">
          <img class="featurette-image img-responsive center-block" data-src="holder.js/500x500/auto" alt="Generic placeholder image">
        </div>
      </div>



      <!-- /END THE FEATURETTES -->
            
</%doc>
      <hr class="featurette-divider">

      <!-- Three columns of text below the carousel -->
      <div class="row">
        <div class="col-lg-4">
          <img class="img-circle" src="/img/bollards2.jpg" alt="Geelong" width="140" height="140">
          <h2>About Geelong</h2>
          <p>Geelong is Victoria's second largest city, located on Corio Bay, and within a short drive from popular beach-front communities on the Bellarine Peninsula as well as being the gateway to the famous Great Ocean Road</p>
          <p><a class="btn btn-default" href="/about/geelong" role="button">More Info &raquo;</a></p>
        </div><!-- /.col-lg-4 -->
        <div class="col-lg-4">
          <img class="img-circle" src="/img/Tux-simple.svg" alt="linux.conf.au" width="140" height="140">
          <h2>linux.conf.au</h2>
          <p>linux.conf.au is widely regarded by delegates as one of the best community run Linux conferences worldwide and is the largest Linux and Open Source Software conference in the Asia-Pacific.</p>
          <p><a class="btn btn-default" href="/about/linux.conf.au" role="button">Read More &raquo;</a></p>
        </div><!-- /.col-lg-4 -->
        <div class="col-lg-4">
          <img class="img-circle" src="/img/ThePier-Crop.png" alt="Sponsorship" width="140" height="140">
          <h2>Sponsorship</h2>
          <p>Our Sponsors help make linux.conf.au become the awesome conference everyone comes back to year after year. Come see who's on board this year, or find out how to get in contact with us</p>
          <p><a class="btn btn-default" href="/sponsors/sponsors" role="button">Sponsorship &raquo;</a></p>
        </div><!-- /.col-lg-4 -->
      </div><!-- /.row -->
    </div><!-- /.container marketing -->


      <!-- FOOTER -->
      <footer>
        <p style="text-align: center;">&copy; 2015 linux.conf.au 2016 and <a href="http://linux.org.au">Linux Australia</a> &middot; Linux is a registered trademark of Linus Torvalds &middot; <a href="/sitemap">Sitemap</a></p>
        <p class="pull-right"><a href="#">Back to top</a></p>
      </footer>

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

