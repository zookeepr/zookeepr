<% menu %>
<h2><% c.db_content.title %></h2>

% if c.is_news:
<p class="submitted">
Submitted on <% c.db_content.creation_timestamp.strftime("%Y-%m-%d&nbsp;%H:%M") %>
</p>
% #endif


<% body %>

<%method title>
<% c.db_content.title %> - <& PARENT:title &>
</%method>

<%init>

import re
menu = ''
findh3 = re.compile('(<h3>(.+?)</h3>)', re.IGNORECASE|re.DOTALL|re.MULTILINE)
h3 = findh3.findall(c.db_content.body)
body = c.db_content.body
if h3.__len__() > 0:
    simple_title = ''
    menu = '<div class="contents"><h3>Contents</h3><ul>'
    for match in h3:
        simple_title = re.compile('([^a-zA-Z])').sub('', match[1])
        body = re.compile(match[0]).sub(r'<a name="' + simple_title + '"></a>\g<0>', body)
        menu += '<li><a href="#' + simple_title + '">' + match[1] + '</a></li>'
    menu += '</ul></div>'

</%init>

<%method big_promotion>
%directory = h.featured_image(c.db_content.title, big = True)
%if directory is not False:
			<div class = 'news_banner'>
				<div class = 'news_banner_left'>
					<a href = '/media/news/<% c.db_content.id %>'><img src = '<% directory %>/1.png' alt="<% c.db_content.title %>" title="<% c.db_content.title %>"></a>
				</div>
				<div class = 'news_banner_right'>
					<a href = '/media/news/<% c.db_content.id %>'><img src = '<% directory %>/3.png' alt="<% c.db_content.title %>" title="<% c.db_content.title %>"></a>
				</div>
				<a href = '/media/news/<% c.db_content.id %>'>
					<img src = '<% directory %>/2.png' alt="<% c.db_content.title %>" title="<% c.db_content.title %>">
				</a>
			</div>
%#endif
</%method>

<%method extra_head>
%directory = h.featured_image(c.db_content.title, big = True)
%if directory is not False:
<style type="text/css">
.content
{
    background-image: url(/images/content_bg_tall.png);
}
</style>
%#endif
</%method>
