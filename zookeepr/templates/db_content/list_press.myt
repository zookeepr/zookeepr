<h1>Linux.conf.au in the press</h1>


% for d in c.db_content_collection:
<h3><% h.link_to(d.title, url=d.url) %></h3>
<p class="submitted">
<% d.url |h%>, submitted on <% d.creation_timestamp.strftime("%Y-%m-%d&nbsp;%H:%M") %>
</p>
%   if d.body != '':
<blockquote><% d.body %></blockquote>
%   #endif
% #endfor

<%python>
if c.db_content_pages.current.previous:
    m.write(h.link_to('Previous page', url=h.url(page=c.db_content_pages.current.previous)) + '  ')
if c.db_content_pages.current.next:
    m.write(h.link_to('Next page', url=h.url(page=c.db_content_pages.current.next)))
</%python>

<%method title>
In the press - <& PARENT:title &>
</%method>


<%init>
</%init>
