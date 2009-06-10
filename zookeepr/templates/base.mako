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
  <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.3/jquery.min.js"></script>          
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
  </script>
  ${self.extra_head()}
</head>

  <div id = "container">
    <div id = "logo">
      <a href="/"><img src="/images/logo.jpg" style="border: 0;" alt="linux.conf.au" /></a>
    </div>
    <div id = 'main_menu'>
      ${self.big_promotion()}
      <%include file="/nav.mako" />
      <%include file="/subnav.mako" />
    </div>
    
    <!-- start content -->
    <div id="wrapper">
      <div id="leftcol">
% if h.url_for() == '/':
    <%include file="/leftcol/home.mako" />
% else:
    <%include file="/leftcol/default.mako" />
% endif

## Toolbox links
% if h.auth.authorized(h.auth.has_organiser_role):
        <div class = 'yellowbox'>
          <div class="boxheader">
            <h1>Toolbox</h1>
            <ul>
              <li>${ h.link_to('Admin', url=h.url_for(controller='admin')) }</li>
%   if c.db_content and not h.url_for().endswith('edit'):
             <li>${ h.link_to('Edit page', url=h.url_for(controller='db_content', action='edit', id=c.db_content.id)) }</li>
%   endif
            </ul>
          </div>
       </div>
% endif
      </div>
      <div id="content">
    <div id="flash">
<% messages = h.get_flashes() %>
%if messages:
%   for (category, msgs) in messages.iteritems():
        <div class="message message-${ h.computer_title(category) }">
%       if len(msgs) is 1:
            <p>${ msgs[0] }</p>
%       else:
            <ul>
%          for msg in msgs:
                <li>${ msg }</li>
%          endfor
            </ul>
%       endif
        </div>
%   endfor
%endif
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

% if h.url_for() == '/':
  <div id="sponsors">
    <p>Thanks to our Emperor Penguin Sponsors:</p>
    <p><a href="http://www.internetnz.org.nz"><img src="/sponsors/InternetNZ.png" alt="InternetNZ" title="Internet NZ works to keep the Internet open and uncaptureable, protecting and promoting the Internet for New Zealand." /></a></p>
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
