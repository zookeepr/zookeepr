<%def name="title()">${ h.lca_info["event_byline"] }</%def>
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
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html lang="en-us">
    <head>
        <title>${ self.title() }</title>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <link rel="shortcut icon" href="/images/favicon.ico" type="image/x-icon">
        <link rel="stylesheet" media="screen, projection" href="/screen.css" type="text/css" />
        <link rel="stylesheet" media="screen" href="/css/lightbox.css" type="text/css" />
        <link rel="stylesheet" media="print" href="/print.css" type="text/css" />
        <script type="text/javascript" src="/jquery.min.js"></script>
        <script type="text/javascript" src="/js/jquery.cross-slide.min.js"></script>
        <link href="/media/news/rss" rel="alternate" type="application/rss+xml" title="LCA2011 News">

        ${self.extra_head()}
        <script type="text/javascript">
            jQuery(document).ready(function() {
                jQuery("#flash > div").hide().fadeIn(3500);
                jQuery("#flash > div").fadeTo(3000, 0.3);
                jQuery("#flash > div").hover(function() {
                    jQuery(this).fadeTo(250, 1);
                },function(){
                    jQuery(this).fadeTo(250, 0.3);
                });
            });
        </script>
%if len(h.lca_info['sponsors']['slideshow']):
        <script type="text/javascript">
            jQuery(function($) {
                jQuery('#sponsorsother').crossSlide({
                    sleep: 5,
                    fade: 1,
                    shuffle: 1
                }, [
%  for sponsor in h.lca_info['sponsors']['slideshow']:
                    { src: '${ sponsor['src'] }', alt: '${ sponsor['name'] }' },
%  endfor
                ]);
            });
        </script>
%endif
    </head>
<body>
  ${self.extra_body()}
  <div id="wrapper">
    <div id="head">
      <div id="page-logo">
        <img src="/images/logo.png">
      </div>
      <div>
      </div>
      <div id="page-title">${ h.lca_info['event_name'] }</div>
      <div id="page-subtitle">A ${ h.lca_info['event_parent_organisation'] } Conference</div>
    </div>
    <div id="columns">
      <div id="col-left">
        <div id="sidebar">
          <h3>Toolbox</h3>
            <!-- block-content -->
            <%include file="/leftcol/toolbox.mako" args="parent=self" />
            <!-- /block-content -->

          <h3>News</h3>
            <!-- block-content -->
            <%include file="/leftcol/news.mako" />
            <!-- /block-content -->

          <h3>In the press</h3>
            <!-- block-content -->
            <%include file="/leftcol/in_the_press.mako" />
            <!-- /block-content -->

%if len(h.lca_info['sponsors']['top']):
          <h3>Our Emperor Sponsors</h3>
          <ul>
% for sponsor in h.lca_info['sponsors']['top']:
            <li><a href="${ sponsor['url'] }"><img src="${ sponsor['src'] }" alt="${ sponsor['name'] }"></a></li>
% endfor
          </ul>
%endif
%if len(h.lca_info['sponsors']['slideshow']):
          <h3>Other Sponsors</h3>
          <div id="sponsorsother" style="width: 200px; height:200px; margin:5px;">
            <img src="${ h.lca_info['sponsors']['slideshow'][0]['src'] }" alt="${ h.lca_info['sponsors']['slideshow'][0]['name'] }">
          </div>
%endif
        </div>
      </div>

      <div id="col-right">
        <div id="navigation">
          <%include file="/nav.mako" />
          <%include file="/subnav.mako" />
          <%include file="/subsubnav.mako" />
        </div>
        <div id="content">
          <%include file="/flash.mako" />
          ${next.body()}
        </div>
        <div id="footer">© 2011 Zookeepr</div>
      </div>
    </div>
  </div>
  <script src="/js/prototype.js" type="text/javascript"></script>
  <script src="/js/scriptaculous.js?load=effects,builder" type="text/javascript"></script>
  <script src="/js/lightbox.js" type="text/javascript"></script>

%if not h.debug():
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
%endif
</body>
</html>

