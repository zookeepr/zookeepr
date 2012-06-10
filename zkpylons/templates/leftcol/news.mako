%if len(c.db_content_news) > 0:
			<ul>
%   for d in c.db_content_news:
	<li>${ h.link_to(d.title, url='/media/news/' + str(d.id)) } <div class="date">(${ d.creation_timestamp.strftime("%Y-%m-%d") })</div></li>
%   endfor
			</ul>
%else:
<p style="font-size: small;"><em>Currently no news...</em></p>
%endif
			<p class = 'more'><a href = '/media/news'>More news...</a></p>
