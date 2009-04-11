<%inherit file="/base.mako" />

<h2>
${ h.lca_info['event_name'] } News<a href="${h.url_for(action='rss_news')}"><img class = 'feedicon' src = '/images/feedicon_16.png' alt='Subscribe to feed' title='Subscribe to feed' /></a>
</h2>

%for d in c.db_content_collection:
<h2>${ h.link_to(d.title, url=h.url_for(action='view', id=d.id)) }</h2>
<p class="submitted">
Submitted on ${ d.creation_timestamp.strftime("%Y-%m-%d %H:%M") }
</p>
<% (teaser, read_more) = h.make_teaser(d.body) %>
${ teaser |n}
%   if read_more:
<p>${ h.link_to('Read full article', url=h.url_for(action='view', id=d.id)) }</p>
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
News -
 ${ caller.title() }
</%def>
