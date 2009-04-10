		<div class = 'yellowbox'>
				<div class="boxheader">
					<div class="rss"><a href="/media/news/rss"><img src="images/rss.gif" border="0" alt="RSS" /></a></div>
			<h1>LCA News</h1>
			<ul>
% for d in c.db_content_news:
	<li><% h.link_to(d.title, url='/media/news/' + str(d.id)) %> <div class="date">(<% d.creation_timestamp.strftime("%Y-%m-%d") %>)</div></li>
% #endfor
			</ul>
			<p class = 'more'><a href = '/media/news'>More news...</a></p>

                                 </div>
		</div>
		<div class = 'yellowbox'>
				<div class="boxheader">
			<h1>News Elsewhere</h1>
			<ul>
% for d in c.db_content_press:
				<li><a href = '<% d.url |h %>' class = 'external'><% d.title %></a><div class="date">(<% h.domain_only(d.url) %> - <% d.creation_timestamp.strftime("%Y-%m-%d") %>)</div></li>
% #endfor
			</ul>
			<p class = 'more'><a href = '/media/in_the_press'>More items...</a></p>
				</div>
		</div>
