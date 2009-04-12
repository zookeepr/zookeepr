<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<%!
    title = 'linux.conf.au 2010 | 18 - 23 Jan | Follow the signs!'
%>

<%def name="extra_head()">
    ## Defined in children
</%def>
<%def name="big_promotion()">
    ## Defined in children
</%def>

<html lang="en-us">
<head>
  <title>${self.attr.title}</title>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <link rel="shortcut icon" href="/images/favicon.ico" type="image/x-icon">
  <link rel="stylesheet" media="screen" href="/penguinsvisiting.css" type="text/css">
  <link href="/media/news/rss" rel="alternate" type="application/rss+xml" title="LCA2010 News">
  <!--[if lt IE 7]>
  <link rel="stylesheet" media="screen" href="/ie.css" type="text/css">
  <![endif]-->
  ${self.extra_head()}
</head>

  <div id = "container">
    <div id = "logo">
      <a href="/"><img src="/images/logo.jpg" border="0" alt="linux.conf.au" /></a>
    </div>
    <div id = 'main_menu'>
      ${self.big_promotion()}
      <%include file="/nav.mako" />
    </div>
    
    <!-- start content -->
    <div id="wrapper">
      <div id="leftcol">

% if h.url_for() == '/':
    <%include file="/leftcol/home.mako" />
% else:
    <%include file="/leftcol/default.mako" />
% endif
      </div>
      <div id="content">
    <div id="flash">
${ h.session.get('flash') }
    </div>
${next.body()}
      </div>
    <!-- end content -->


##% if not h.url()().endswith('/sponsors/sponsors') and not h.url()().endswith('/media/news/61'):
##         <div class='sponsors_footer'>
##       <a href="/sponsors/sponsors"><img src="/sponsors/HP-front.png" alt="Hewlett-Packard Logo"></a>
##       <a href="/sponsors/sponsors"><img src="/sponsors/IBM-front.png" alt="IBM Logo"></a>
##         </div>
##% #endif
    </div>
    <div id = "push"></div>
  </div>


  <div id = 'footer'>
    <div class = 'copyright'>
  &copy; 2009 <a href="http://linux.conf.au/">linux.conf.au 2010</a> and <a href="http://www.linux.org.au">Linux Australia</a> | Linux is a registered trademark of Linus Torvalds | <a href="http://validator.w3.org/check?uri=referer">Valid XHTML 1.0</a>
    </div>
  </div>

<script type="text/javascript">
    var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
    document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
</script>

<script type="text/javascript">
    try {
        var pageTracker = _gat._getTracker("UA-8037859-1");
        pageTracker._trackPageview();
    } catch(err) {}
</script>

</body>
</html>
