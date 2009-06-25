<%inherit file="/base.mako" />
<%
import re
findh3 = re.compile('(<h3>(.+?)</h3>)', re.IGNORECASE|re.DOTALL|re.MULTILINE)
h3 = findh3.findall(c.db_content.body)
body = c.db_content.body
if h3.__len__() > 0:
    simple_title = ''
    for match in h3:
        simple_title = re.compile('([^a-zA-Z])').sub('', match[1])
        body = re.compile(match[0]).sub(r'<a name="' + simple_title + '"></a>\g<0>', body)
%>

<h2>${ c.db_content.title }</h2>

% if c.db_content.is_news():
<p class="submitted">
Submitted on ${ c.db_content.creation_timestamp.strftime("%Y-%m-%d&nbsp;%H:%M") |n }
</p>
div style="float: right; vertical-align: middle">
    <script type="text/javascript">
    digg_bgcolor = '#FFFFFF';
    digg_title = '${ d.title } - ${ parent.title() }';
    digg_url = '${ h.lca_info['event_permalink'] }${ h.url_for(action='view', id=d.id) }';
    </script>
    <script src="/js/diggthis.js" type="text/javascript"></script>
<a style="vertical-align:top;" href="http://delicious.com/save" onclick="window.open('http://delicious.com/save?v=5&amp;noui&amp;jump=close&amp;url='+encodeURIComponent(${ h.lca_info["event_permalink"]}${h.url_for(action='view', id=d.id)})+'&amp;title='+encodeURIComponent(${ d.title } - ${ parent.title() }), 'delicious','toolbar=no,width=550,height=550'); return false;"><img style="vertical-align: top; padding-right: 5px" src="/images/delicious.small.gif" height="10" width="10" alt="Delicious" />Delicious</a>
</div>
% endif


${ body |n}


<%def name="title()">
${ c.db_content.title } -
 ${ parent.title() }
</%def>

<%def name="big_promotion()">
<% directory = h.featured_image(c.db_content.title, big = True) %>
%if directory is not False:
			<div class = 'news_banner'>
%  if h.os.path.isfile(directory + "/3.png"):
				<div class = 'news_banner_left'>
					<a href = '/media/news/${ c.db_content.id }'><img src = '${ directory }/1.png' alt="${ c.db_content.title }" title="${ c.db_content.title }"></a>
				</div>
%  endif
%  if h.os.path.isfile(directory + "/3.png"):
				<div class = 'news_banner_right'>
					<a href = '/media/news/${ c.db_content.id }'><img src = '${ directory }/3.png' alt="${ c.db_content.title }" title="${ c.db_content.title }"></a>
				</div>
%  endif
				<a href = '/media/news/${ c.db_content.id }'>
					<img src = '${ directory }/2.png' alt="${ c.db_content.title }" title="${ c.db_content.title }">
				</a>
			</div>
  <br /><br />
%endif
</%def>

<%def name="extra_head()">
<% directory = h.featured_image(c.db_content.title, big = True) %>
%if directory is not False:
<style type="text/css">
.content
{
    background-image: url(/images/content_bg_tall.png);
}
</style>
%endif
</%def>
