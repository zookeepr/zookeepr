<h2>linux.conf.au in the press</h2>


% for d in c.db_content_collection:
<h3><% h.link_to(d.title, url=d.url) %></h3>
<p class="submitted">
<% d.url %>, submitted on <% d.creation_timestamp.strftime("%Y-%m-%d&nbsp;%H:%M") %>
</p>
%   if d.body != '':
<blockquote><% d.body %></blockquote>
%   #endif
% #endfor

<%method title>
In the press - <& PARENT:title &>
</%method>


<%init>
</%init>
