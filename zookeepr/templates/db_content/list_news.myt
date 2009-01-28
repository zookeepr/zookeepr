<h1>linux.conf.au 2010 News</h1>

% for d in c.db_content_collection:
<h2><% h.link_to(d.title, url='/media/news/' + str(d.id)) %></h2>
<p class="submitted">
Submitted on <% d.creation_timestamp.strftime("%Y-%m-%d&nbsp;%H:%M") %>
</p>
% (teaser, read_more) = h.make_teaser(d.body)
<% teaser %>
% if read_more:
<p><% h.link_to('Read full article', url='/media/news/' + str(d.id)) %></p>
% #endif
% #endfor

<%python>
if c.db_content_pages.current.previous:
    m.write(h.link_to('Previous page', url=h.url(page=c.db_content_pages.current.previous)) + '  ')
if c.db_content_pages.current.next:
    m.write(h.link_to('Next page', url=h.url(page=c.db_content_pages.current.next)))
</%python>


<%method title>
News - <& PARENT:title &>
</%method>

<%init>
</%init>
