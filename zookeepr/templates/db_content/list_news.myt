<h2>linux.conf.au 2009 News</h2>


% for d in c.db_content_collection:
<h3><% h.link_to(d.title, url='/media/news/' + str(d.id)) %></h3>
<p class="submitted">
Submitted on <% d.creation_timestamp.strftime("%Y-%m-%d&nbsp;%H:%M") %>
</p>
% (teaser, read_more) = h.make_teaser(d.body)
<% teaser %>
% if read_more:
<p><% h.link_to('Read full article', url='/media/news/' + str(d.id)) %></p>
% #endif
% #endfor

<%method title>
News - <& PARENT:title &>
</%method>

<%init>
</%init>
