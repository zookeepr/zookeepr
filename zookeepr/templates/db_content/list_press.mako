<%inherit file="/base.mako" />
<h2>${ h.lca_info['event_name'] } in the press</h2>

%if len(c.db_content_collection) is 0:
<p>Sorry, there are currently no recorded items in the press.</p>
%endif

%for d in c.db_content_collection:
<h3>${ h.link_to(d.title, url=d.url) }</h3>
<div style="float: right">
    <script type="text/javascript">
    digg_bgcolor = '#FFFFFF';
    digg_title = '${ d.title } - ${ parent.title() }';
    digg_url = '${ h.lca_info['event_permalink'] }${ h.url_for(action='view', id=d.id) }';
    </script>
    <script src="/js/diggthis.js" type="text/javascript"></script>
<a style="vertical-align:top;" href="http://delicious.com/save" onclick="window.open('http://delicious.com/save?v=5&amp;noui&amp;jump=close&amp;url='+encodeURIComponent(${ h.lca_info["event_permalink"]}${h.url_for(action='view', id=d.id)})+'&amp;title='+encodeURIComponent(${ d.title } - ${ parent.title() }), 'delicious','toolbar=no,width=550,height=550'); return false;"><img style="vertical-align: top; padding-right: 5px" src="/images/delicious.small.gif" height="10" width="10" alt="Delicious" />Delicious</a>
</div>
<p class="submitted">
${ d.url |h}, submitted on ${ d.creation_timestamp.strftime("%Y-%m-%d %H:%M") }
</p>
%   if d.body != '':
<blockquote>${ d.body |n}</blockquote>
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
In the press -
 ${ parent.title() }
</%def>
