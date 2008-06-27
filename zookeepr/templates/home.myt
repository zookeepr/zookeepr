<h2>linux.conf.au</h2>

% if featured.__len__() > 0:
<div class="featured_news">
%   for d in featured:
<a href="/media/news/<% d.id %>"><img src="<% h.featured_image(d.title) %>" alt="<% d.title %>" title="<% d.title %>" /></a>
%   #endfor
</div>
% #endif

<h3>News</h3>
% for d in c.db_content_collection:
<p><% h.link_to(d.title, url='/media/news/' + str(d.id)) %><br>
<span class="submitted">Submitted on <% d.creation_timestamp.strftime("%Y-%m-%d&nbsp;%H:%M") %></span>
</p>
% #endfor

<h3>In the press</h3>
% for d in c.db_content_collection:
<p><% h.link_to(d.title, url=d.url) %><br>
<span class="submitted"><% d.url %>, submitted on <% d.creation_timestamp.strftime("%Y-%m-%d&nbsp;%H:%M") %></span>
</p>
% #endfor

<%init>
featured = []
for d in c.db_content_collection:
    if h.featured_image(d.title) is not False:
        featured.append(d)
</%init>

<%method big_promotion>
for d in c.db_content_collection:
    if h.featured_image(d.title, big = True) is not False:
        <a href="/media/news/<% d.id %>"><img src="<% h.featured_image(d.title) %>" alt="<% d.title %>" title="<% d.title %>" /></a>
</%method>
