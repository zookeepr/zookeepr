		<img src = '/images/heightfix.png' class = 'heightfix' alt = ''>

		<ul class = 'news_hero_items'>
% for d in featured:
			<li><a href = '/media/news/<% d.id %>'><img src = '<% h.featured_image(d.title) %>' alt = '<% d.title %>'></a></li>
% #endfor
% for i in range(count,limit):
			<li><img src = '/images/news_item_blank.png' alt = ''></li>
%
		</ul>


		<div class = 'home_news'>
			<h3 class = 'news_item_list_heading'><a href = '/media/news'>News updates</a><a href="/media/news/rss"><img class = 'feedicon' src = '/images/feedicon_16.png' alt="Subscribe to feed" title="Subscribe to feed"></a></h3>
			<ul class = 'news_item_list'>
% for d in c.db_content_news:
	<li><% h.link_to(d.title, url='/media/news/' + str(d.id)) %><br><span><% d.creation_timestamp.strftime("%Y-%m-%d") %></span></li>
% #endfor
				<li class = 'more_link'><a href = '/media/news'>More news...</a></li>
			</ul>

			<h3 class = 'news_item_list_heading'><a href = '/media/in_the_press'>LCA elsewhere</a></h3>
			<ul class = 'news_item_list'>
% for d in c.db_content_press:
				<li><a href = '<% d.url |h %>' class = 'external'><% d.title %></a><br><span><% h.domain_only(d.url) %> - <% d.creation_timestamp.strftime("%Y-%m-%d") %></span></li>
% #endfor
				<li class = 'more_link'><a href = '/media/in_the_press'>More items...</a></li>
			</ul>
		</div>


		<div class = 'home_content' >
			<h3 class='news_page_text_heading'>Congratulations to Wellington for 2010!</h3>
				<p class='news_page_text'>
					<a href="http://www.penguinsvisiting.org.nz/"><img src="http://www.penguinsvisiting.org.nz/images/logo.jpg" style="float: left; padding: 1em;" alt=""></a>
					In January 2010, linux.conf.au will be visiting Wellington, New Zealand, home of the little blue penguin or Korora as they are called in Maori, New Zealand's indigenous language. What better place to bring the world's biggest gathering of Linux enthusiasts?
				</p>
				<p class='news_page_text'>
					Visit: <a href="http://www.penguinsvisiting.org.nz/">http://www.penguinsvisiting.org.nz/</a>
				</p>
			</h3>
			<div style="clear: left;"></div>
			<h3 class = 'news_page_text_heading'>Welcome!</h3>
			<p class = 'news_page_text'>
				linux.conf.au is marching south to Hobart, Tasmania for its 10th anniversary in 2009!  It is widely regarded as one of the world's best technical conferences, and this year it will be held in one of the most unique locations, for the first time.
			</p>

			<h3 class = 'news_page_text_heading'>When</h3>
			<p class = 'news_page_text'>
				linux.conf.au runs for a whole week starting on Monday January 19th going through til the 24th. The main programme starts on Wednesday January 21st 2009 and runs through Wednesday, Thursday and Friday.  The event finishes with a spectacle of colour and activity with the Open Day on Saturday January 24 2009.  Miniconfs will be held as usual on Monday 19th and Tuesday 20th.
			</p>
			<h3 class = 'news_page_text_heading'>Where</h3>
			<p class = 'news_page_text'>
				The University of Tasmania's Sandy Bay campus will play host to this year's activities.
			</p>
			<h3 class = 'news_page_text_heading'>More</h3>
			<p class = 'news_page_text'>
				Keep up to date by subscribing to <a href="/media/news/rss">our news feed here</a>, or join our mailing lists: <i><a href="http://lists.linux.org.au/listinfo/lca-announce">announce</a>, <a href="http://lists.marchsouth.org/mailman/listinfo/lca09_chat_lists.marchsouth.org">chat</a></i>. For more information, please visit our <a href="/contact">contact</a> section.
			</p>

			<p class = 'news_page_text'>
				Don't miss it - March South to Tasmania for linux.conf.au 2009!
			</p>
		</div>


<%init>
featured = []
count = 0
limit = 4
for d in c.db_content_news_all:
    if (h.featured_image(d.title) is not False) and (count < limit):
        featured.append(d)
        count += 1
</%init>

<%method big_promotion>
%for d in c.db_content_news_all:
%    directory = h.featured_image(d.title, big = True)
%    if directory is not False:
			<div class = 'news_banner'>
				<div class = 'news_banner_left'>
					<a href = '/media/news/<% d.id %>'><img src = '<% directory %>/1.png' alt="<% d.title %>" title="<% d.title %>"></a>
				</div>
				<div class = 'news_banner_right'>
					<a href = '/media/news/<% d.id %>'><img src = '<% directory %>/3.png' alt="<% d.title %>" title="<% d.title %>"></a>
				</div>
				<a href = '/media/news/<% d.id %>'>
					<img src = '<% directory %>/2.png' alt="<% d.title %>" title="<% d.title %>">
				</a>
			</div>
%        break
%    #endif
%#endfor
</%method>

<%method extra_head>
%for d in c.db_content_news_all:
%    directory = h.featured_image(d.title, big = True)
%    if directory is not False:
<style type="text/css">
.content
{
    background-image: url(/images/content_bg_tall.png);
}
</style>
%        break
%    #endif
%#endfor
</%method>
