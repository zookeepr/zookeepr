<%inherit file="/base.mako" />
<%def name="extra_head()">
    <!--[if IE]><script language="javascript" type="text/javascript" src="/js/flot/excanvas.min.js"></script><![endif]-->
    <script language="javascript" type="text/javascript" src="/js/flot/jquery.flot.js"></script>
    <script language="javascript" type="text/javascript" src="/js/flot/jquery.flot.pie.js"></script>
</%def>

<%
  import re 
  grand_total = 0
  count = 0
  graph_data = []
%>

    <h2>List products</h2>
% if len(c.product_categories) > 0:
    <h3>Categories:</h3> <ul>
%   for category in c.product_categories:
      <li>${h.link_to(category.name,
          url=h.url_for(controller='product_category', id=category.id,
          action='stats'))}
%   endfor
    </ul><br>
% endif

<p>${ h.link_to('New category', url=h.url_for(controller='product', action='new')) }</p>

<%def name="contents()">
<%
  menu = ''

  import re

  for category in c.product_categories:
    simple_title = re.compile('([^a-zA-Z0-9])').sub('', category.name) 
    menu += '<li><a href="#' + simple_title + '">' + category.name + ' products</a></li>' 
  return menu
%>
</%def>
<%def name="title()">
Products -
 ${ parent.title() }
</%def>

