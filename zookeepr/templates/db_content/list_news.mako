<%inherit file="/base.mako" />
<h1>${ h.lca_info['event_name'] } News</h1>

%if len(c.db_content_collection) is 0:
<p>Sorry, there are currently no news posts.</p>
%endif

% for d in c.db_content_collection:
<h2>${ h.link_to(d.title, url=h.url_for(action="view", id=d.id)) }</h2>
<p class="submitted">
Submitted on ${ d.creation_timestamp.strftime("%Y-%m-%d %H:%M") }
</p>
<div style="float: right; vertical-align: middle">
    <script type="text/javascript">
    digg_bgcolor = '#FFFFFF';
    digg_title = '${ d.title } - ${ parent.title() }';
    digg_url = '${ h.lca_info['event_permalink'] }${ h.url_for(action='view', id=d.id) }';
    </script>
    <script src="/js/diggthis.js" type="text/javascript"></script>
<a style="vertical-align:top;" href="http://delicious.com/save" onclick="window.open('http://delicious.com/save?v=5&amp;noui&amp;jump=close&amp;url='+encodeURIComponent(${ h.lca_info["event_permalink"]}${h.url_for(action='view', id=d.id)})+'&amp;title='+encodeURIComponent(${ d.title } - ${ parent.title() }), 'delicious','toolbar=no,width=550,height=550'); return false;"><img style="vertical-align: top; padding-right: 5px" src="/images/delicious.small.gif" height="10" width="10" alt="Delicious" />Delicious</a>
</div>
<% (teaser, read_more) = h.make_teaser(d.body) %>
${ teaser |n}
%   if read_more:
<p>${ h.link_to('Read full article', url=h.url_for(action='view', id=d.id)) }</p>
%   endif
%endfor

% if c.result == True:
<p>
% if c.db_content_pages.next_page:
    <span style="float: right;">${ h.link_to('Next page', url=h.url_for(page=c.db_content_pages.next_page)) }</span>
% endif
% if c.db_content_pages.previous_page:
    <span>${ h.link_to('Previous page', url=h.url_for(page=c.db_content_pages.previous_page)) + '  ' }</span>
% endif
</p>
% endif

<%def name="title()">
News -
 ${ parent.title() }
</%def>
