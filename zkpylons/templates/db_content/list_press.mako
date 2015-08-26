<%inherit file="/base.mako" />
<%namespace file="../bookmark_submit.mako" name="bookmark_submit" inheritable="True"/>

<h2>${ c.config.get('event_name') } in the press</h2>

%if len(c.db_content_collection) is 0:
<p>Sorry, there are currently no recorded items in the press.</p>
%endif

%for d in c.db_content_collection:
<h3>${ h.link_to(d.title, url=d.url) }</h3>
<div style="float: right">
${ bookmark_submit.bookmark_submit(d.url, d.title) }
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

<%def name="short_title()"><%
  return "In the press"
%></%def>
<%def name="title()">
In the press -
 ${ parent.title() }
</%def>
