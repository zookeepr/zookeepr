<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
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


<html lang="en-us">
<head>
  <title>${ self.title() }</title>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <link rel="shortcut icon" href="/images/favicon.ico" type="image/x-icon">
  <link rel="stylesheet" media="screen" href="/penguinsvisiting.css" type="text/css">
  <link rel="stylesheet" media="screen" href="/css/lightbox.css" type="text/css">
  <link rel="stylesheet" media="print" href="/print.css" type="text/css">
  <script type="text/javascript" src="/jquery.min.js"></script>          
  <link href="/media/news/rss" rel="alternate" type="application/rss+xml" title="LCA2011 News">
  <!--[if lt IE 7]>
  <link rel="stylesheet" media="screen" href="/ie.css" type="text/css">
  <![endif]-->
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

</head>

${self.extra_body()}


<div id="netv-main">
        <div class="netv-sheet">
            <div class="netv-sheet-tl"></div>
            <div class="netv-sheet-tr"></div>
            <div class="netv-sheet-bl"></div>
            <div class="netv-sheet-br"></div>
            <div class="netv-sheet-tc"></div>
            <div class="netv-sheet-bc"></div>
            <div class="netv-sheet-cl"></div>
            <div class="netv-sheet-cr"></div>
            <div class="netv-sheet-cc"></div>
            <div class="netv-sheet-body">
                <div class="netv-header">
                    <div class="netv-header-jpeg"></div>
                </div>
                <div class="netv-nav">
                	<div class="l"></div>
                	<div class="r"></div>

			        <%include file="/nav.mako" />

                </div>
                <div class="netv-content-layout">
                    <div class="netv-content-layout-row">
                        <div class="netv-layout-cell netv-sidebar1">
                            <div class="netv-vmenublock">
                                <div class="netv-vmenublock-tl"></div>
                                <div class="netv-vmenublock-tr"></div>
                                <div class="netv-vmenublock-bl"></div>
                                <div class="netv-vmenublock-br"></div>
                                <div class="netv-vmenublock-tc"></div>
                                <div class="netv-vmenublock-bc"></div>
                                <div class="netv-vmenublock-cl"></div>
                                <div class="netv-vmenublock-cr"></div>
                                <div class="netv-vmenublock-cc"></div>
                                <div class="netv-vmenublock-body">
                                            <div class="netv-vmenublockcontent">
                                                <div class="netv-vmenublockcontent-body">
                                            <!-- block-content -->

					    <%include file="/leftcol/toolbox.mako" args="parent=self" />
							      
                                            		<div class="cleared"></div>
                                                </div>
                                            </div>
                            		<div class="cleared"></div>
                                </div>
                            </div>
                            <div class="netv-block">
                                <div class="netv-block-tl"></div>
                                <div class="netv-block-tr"></div>
                                <div class="netv-block-bl"></div>
                                <div class="netv-block-br"></div>
                                <div class="netv-block-tc"></div>
                                <div class="netv-block-bc"></div>
                                <div class="netv-block-cl"></div>
                                <div class="netv-block-cr"></div>
                                <div class="netv-block-cc"></div>
                                <div class="netv-block-body">
                                            <div class="netv-blockheader">
                                                <div class="l"></div>
                                                <div class="r"></div>
                                                 <div class="t">Newsletter</div>
                                            </div>
                                            <div class="netv-blockcontent">
                                                <div class="netv-blockcontent-body">
                                            <!-- block-content -->
                                                            <div><form method="get" id="newsletterform" action="javascript:void(0)">
                                                            <input type="text" value="" name="email" id="s" style="width: 95%;" />
                                                            <span class="netv-button-wrapper">
                                                            	<span class="l"> </span>
                                                            	<span class="r"> </span>
                                                            	<input class="netv-button" type="submit" name="search" value="Subscribe" />
                                                            </span>
                                                            
                                                            </form></div>
                                            <!-- /block-content -->
                                            
                                            		<div class="cleared"></div>
                                                </div>
                                            </div>
                            		<div class="cleared"></div>
                                </div>
                            </div>
                        </div>
                        <div class="netv-layout-cell netv-content">
                            <div class="netv-post">
                                <div class="netv-post-tl"></div>
                                <div class="netv-post-tr"></div>
                                <div class="netv-post-bl"></div>
                                <div class="netv-post-br"></div>
                                <div class="netv-post-tc"></div>
                                <div class="netv-post-bc"></div>
                                <div class="netv-post-cl"></div>
                                <div class="netv-post-cr"></div>
                                <div class="netv-post-cc"></div>
                                <div class="netv-post-body">
                            <div class="netv-post-inner netv-article">
                                            <h2 class="netv-postheader">
                                                <img src="images/postheadericon.png" width="26" height="26" alt="postheadericon" />
                                                Welcome                                            </h2>
                                            <div class="netv-postcontent">
                                                <!-- article-content -->
                                                
                                                
                                                <p>Lorem ipsum dolor sit amet,
                                                <a href="#" title="link">link</a>, <a class="visited" href="#" title="visited link">visited link</a>,
                                                 <a class="hover" href="#" title="hovered link">hovered link</a> consectetuer
                                                adipiscing elit. Quisque sed felis. Aliquam sit amet felis. Mauris semper,
                                                velit semper laoreet dictum, quam diam dictum urna, nec placerat elit nisl
                                                in quam. Etiam augue pede, molestie eget, rhoncus at, convallis ut, eros.</p>
                                                <p>
                                                	<span class="netv-button-wrapper">
                                                		<span class="l"> </span>
                                                		<span class="r"> </span>
                                                		<a class="netv-button" href="javascript:void(0)">Read more...</a>                                                	</span>                                                </p>
                                                <div class="cleared"></div>
                                                <div class="netv-content-layout overview-table">
                                                	<div class="netv-content-layout-row">
                                                		<div class="netv-layout-cell">
                                                      <div class="overview-table-inner">
                                                	      <h4>Support</h4>
                                                						  <p>Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
                                                						  Quisque sed felis. Aliquam sit amet felis. Mauris semper,
                                                						  velit semper laoreet dictum, quam diam dictum urna. </p>
                                                       </div>
                                                		</div><!-- end cell -->
                                                		<div class="netv-layout-cell">
                                                    <div class="overview-table-inner">
                                                		  <h4>Development</h4>
                                                						  <p>Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
                                                						  Quisque sed felis. Aliquam sit amet felis. Mauris semper,
                                                						  velit semper laoreet dictum, quam diam dictum urna. </p>
                                           				  </div>
                                                		</div><!-- end cell -->
                                                		<div class="netv-layout-cell">
                                                    <div class="overview-table-inner">
                                                		  <h4>Strategy</h4>
                                                
                                                						  <p>Lorem ipsum dolor sit amet, consectetuer adipiscing elit.
                                                						  Quisque sed felis. Aliquam sit amet felis. Mauris semper,
                                                						  velit semper laoreet dictum, quam diam dictum urna. </p>
                                                          </div>
                                                		</div><!-- end cell -->
                                                	</div><!-- end row -->
                                                </div><!-- end table -->
                                                    
                                                <!-- /article-content -->
                                            </div>
                                            <div class="cleared"></div>
                            </div>
                            
                            		<div class="cleared"></div>
                                </div>
                            </div>
                            <div class="netv-post">
                                <div class="netv-post-tl"></div>
                                <div class="netv-post-tr"></div>
                                <div class="netv-post-bl"></div>
                                <div class="netv-post-br"></div>
                                <div class="netv-post-tc"></div>
                                <div class="netv-post-bc"></div>
                                <div class="netv-post-cl"></div>
                                <div class="netv-post-cr"></div>
                                <div class="netv-post-cc"></div>
                                <div class="netv-post-body">
                            <div class="netv-post-inner netv-article">
                                            <h2 class="netv-postheader">
                                                <img src="images/postheadericon.png" width="26" height="26" alt="postheadericon" />
                                                Text, <a href="#" rel="bookmark" title="Permanent Link to this Post">Link</a>, <a class="visited" href="#" rel="bookmark" title="Visited Hyperlink">Visited</a>, <a class="hovered" href="#" rel="bookmark" title="Hovered Hyperlink">Hovered</a>                                            </h2>
                                            <div class="netv-postcontent">
                                                <!-- article-content -->
                                                <p>Lorem <sup>superscript</sup> dolor <sub>subscript</sub> amet, consectetuer adipiscing elit, <a href="#" title="test link">test link</a>.
                                                	Nullam dignissim convallis est. Quisque aliquam. <cite>cite</cite>.
                                                	Nunc iaculis suscipit dui. Nam sit amet sem. Aliquam libero nisi, imperdiet at, tincidunt nec, gravida vehicula, nisl.
                                                	Praesent mattis, massa quis luctus fermentum, turpis mi volutpat justo, eu volutpat enim diam eget metus.
                                                	Maecenas ornare tortor. Donec sed tellus eget sapien fringilla nonummy. <acronym title="National Basketball Association">NBA</acronym> Mauris a ante.
                                                	Suspendisse quam sem, consequat at, commodo vitae, feugiat in, nunc.
                                                	Morbi imperdiet augue quis tellus.  <abbr title="Avenue">AVE</abbr></p>
                                                
                                                  <h1>Heading 1</h1>
                                                  <h2>Heading 2</h2>
                                                  <h3>Heading 3</h3>
                                                  <h4>Heading 4</h4>
                                                  <h5>Heading 5</h5>
                                                  <h6>Heading 6</h6>
                                                
                                                    <blockquote>
                                                        <p>
                                                            &#8220;This stylesheet is going to help so freaking much.&#8221;
                                                            <br />
                                                            -Blockquote                                                        </p>
                                                    </blockquote>
                                                  <br />
                                                  <table class="netv-article" border="0" cellspacing="0" cellpadding="0">
                                                  <tbody>
                                                    <tr>
                                                      <th>Header</th>
                                                      <th>Header</th>
                                                      <th>Header</th>
                                                    </tr>
                                                    <tr>
                                                      <td>Data</td>
                                                      <td>Data</td>
                                                      <td>Data</td>
                                                    </tr>
                                                    <tr class="even">
                                                      <td>Data</td>
                                                      <td>Data</td>
                                                      <td>Data</td>
                                                    </tr>
                                                    <tr>
                                                      <td>Data</td>
                                                      <td>Data</td>
                                                      <td>Data</td>
                                                    </tr>
                                                  </tbody></table>
                                                
                                                	<p>
                                                		<span class="netv-button-wrapper">
                                                			<span class="l"> </span>
                                                			<span class="r"> </span>
                                                			<a class="netv-button" href="javascript:void(0)">Join&nbsp;Now!</a>                                                		</span>                                                	</p>
                                                    
                                                <!-- /article-content -->
                                            </div>
                                            <div class="cleared"></div>
                            </div>
                            
                            		<div class="cleared"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="cleared"></div><div class="netv-footer">
                    <div class="netv-footer-inner">
                        <a href="#" class="netv-rss-tag-icon" title="RSS"></a>
                        <div class="netv-footer-text">
  &copy; 2010 <a href="http://linux.conf.au/">linux.conf.au 2011</a> and <a href="http://www.linux.org.au">Linux Australia</a> | Linux is a registered trademark of Linus Torvalds | <a href="http://validator.w3.org/check?uri=referer">Valid XHTML 1.0</a> | <a href="/sitemap">Sitemap</a>
    </div>

                        </div>
                    </div>
                    <div class="netv-footer-background"></div>
                </div>
        		<div class="cleared"></div>
            </div>
        </div>
        <div class="cleared"></div>
        <p class="netv-page-footer">&nbsp;</p>
</div>
    


  <div id = "container">
    <div id = "logo">
      <a href="/"><img src="/images/logo.png" style="border: 0;" alt="linux.conf.au" /></a>
    </div>
    <div id = 'main_menu'>
      <%include file="/subnav.mako" />
      <%include file="/subsubnav.mako" />
    </div>
    
    <!-- start content -->
    <div id="wrapper">
      <div id="leftcol">
% if h.url_for() == '/':
    <%include file="/leftcol/news.mako" />
    <%include file="/leftcol/in_the_press.mako" />
% else:
    <%include file="/leftcol/contents.mako" args="parent=self" />
% endif
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


    </div>
    <div id = "push"><br /><br /><br /><br /></div>
  </div>


  <div id = 'footer'>
    <div id = "footer_logo">
      <img src="/images/sign-and-pole.png" style="border: 0;" alt="Penguins Visiting" />
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
