<%inherit file="/base.mako" />
<h2>${ h.lca_info['event_name'] } in the press</h2>

%for d in c.db_content_collection:
<h3>${ h.link_to(d.title, url=d.url) }</h3>
<p class="submitted">
${ d.url |h}, submitted on ${ d.creation_timestamp.strftime("%Y-%m-%d %H:%M") }
</p>
%   if d.body != '':
<blockquote>${ d.body |n}</blockquote>
%   endif
%endfor

<p>
% if c.db_content_pages.current.next:
    <span style="float: right;">${ h.link_to('Next page', url=h.url_for(page=c.db_content_pages.current.next)) }</span>
% endif
% if c.db_content_pages.current.previous:
    <span>${ h.link_to('Previous page', url=h.url_for(page=c.db_content_pages.current.previous)) + '  ' }</span>
% endif
</p>

<%def name="title()">
In the press -
 ${ caller.title() }
</%def>
