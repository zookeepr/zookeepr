<%inherit file="/base.mako" />
${ c.text | n }
% if hasattr(c, 'sect_text'):
    ${ c.sect_text | n }
% endif

<br>
<p>${ h.link_to("Back to admin list", h.url_for(controller='admin')) }</p>

<%def name="contents()">
<%
  menu = ''

  for (name, link) in c.sects:
    menu += '<li><a href="#' + link + '">' + link + '</li>'
  return menu
%>
</%def>
