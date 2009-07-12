<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<%def name="title()">${ h.lca_info["event_byline"] }</%def>
<%def name="short_title()">
   ## Defined in children
</%def>
<%def name="extra_head()">
    ## Defined in children
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


<html lang="en-us">
<head>
  <title>${ self.title() }</title>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <link rel="shortcut icon" href="/images/favicon.ico" type="image/x-icon">
  <link rel="stylesheet" media="screen" href="/penguinsvisiting.css" type="text/css">
  <link rel="stylesheet" media="screen" href="/css/lightbox.css" type="text/css">
  <link href="/media/news/rss" rel="alternate" type="application/rss+xml" title="LCA2010 News">
  <script type="text/javascript" src="/jquery.min.js"></script>          
  <script src="/js/prototype.js" type="text/javascript"></script>
  <script src="/js/scriptaculous.js?load=effects,builder" type="text/javascript"></script>
  <script src="/js/lightbox.js" type="text/javascript"></script>
  <!--[if lt IE 7]>
  <link rel="stylesheet" media="screen" href="/ie.css" type="text/css">
  <![endif]-->
  <script type="text/javascript">
     $(document).ready(function() {
       $("#flash > div").hide().fadeIn(3500);
       $("#flash > div").fadeTo(3000, 0.3);
       $("#flash > div").hover(function() {
         $(this).fadeTo(250, 1);
       },function(){
         $(this).fadeTo(250, 0.3);
       });

     });
     Event.observe(window,'load',function(){ Lightbox.initialize({googleAnalytics:true,slideTime=15}); });
  </script>
  ${self.extra_head()}
</head>

  <div id = "container">
    <div id = "logo">
      <a href="/"><img src="/images/logo.jpg" style="border: 0;" alt="linux.conf.au" /></a>
    </div>
    <div id = 'main_menu'>
      <%include file="/nav.mako" />
      <%include file="/subnav.mako" />
    </div>
    
    <!-- start content -->
    <div id="wrapper">
      <div id="leftcol">
% if h.url_for() == '/':
    <%include file="/leftcol/news.mako" />
    <%include file="/leftcol/in_the_press.mako" />
% else:
    <%include file="/leftcol/contents.mako" />
% endif
<%include file="/leftcol/toolbox.mako" args="parent=self" />
% if h.url_for() != '/':
    <%include file="/leftcol/top_sponsors.mako" />
% endif
      </div>
      <div id="content">
<%include file="/flash.mako" />
${self.big_promotion()}
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

% if h.url_for() == '/':
  <div id="sponsors">
    <p>Thanks to our Emperor Penguin Sponsors:</p>
    <p><a href="http://www.internetnz.org.nz"><img src="/images/sponsor-InternetNZ.png" alt="InternetNZ" title="Internet NZ works to keep the Internet open and uncaptureable, protecting and promoting the Internet for New Zealand." /></a></p>
  </div>
% endif

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
