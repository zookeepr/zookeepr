		<img src = '/images/heightfix.png' class = 'heightfix' alt = ''>
		<h3 class = 'news_item_list_heading'><a href = '/media/news'>News updates</a><a href="/media/news/rss"><img class = 'feedicon' src = '/images/feedicon_16.png'></a></h3>
		<ul class = 'news_item_list'>
% for d in c.db_content_news:
<li><% h.link_to(d.title, url='/media/news/' + str(d.id)) %><br><span><% d.creation_timestamp.strftime("%Y-%m-%d") %></span></li>
% #endfor
			<li class = 'more_link'><a href = '/media/news'>More news...</a></li>
		</ul>

		<h3 class = 'news_item_list_heading'><a href = '/media/in_the_press'>LCA elsewhere</a></h3>
		<ul class = 'news_item_list'>
% for d in c.db_content_press:
			<li><a href = '<% d.url %>' class = 'external'><% d.title %></a><br><span><% h.domain_only(d.url) %> - <% d.creation_timestamp.strftime("%Y-%m-%d") %></span></li>
% #endfor
			<li class = 'more_link'><a href = '/media/in_the_press'>More items...</a></li>
		</ul>
		<ul class = 'news_hero_items'>
% for d in featured:
			<li><a href = '/media/news/<% d.id %>'><img src = '<% h.featured_image(d.title) %>' alt = '<% d.title %>'></a></li>
% #endfor
% for i in range(count,limit):
			<li><img src = '/images/news_item_blank.png' alt = ''></li>
%
		</ul>
		
		<h3 class = 'news_page_text_heading'>Welcome!</h3>
		<p class = 'news_page_text'>Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Ut lacus. Donec pede quam, cursus bibendum, dapibus eget, tincidunt id, metus. Nam porttitor dignissim lorem. Sed at odio. Nunc nec elit sit amet neque condimentum luctus. Nunc facilisis risus eu leo. In sed sem eu justo ullamcorper sodales. Suspendisse ac arcu. Ut at dui ac felis condimentum adipiscing. Cras aliquet nisl ac orci.</p>

		<p class = 'news_page_text'>Mauris tellus. Sed a leo non mi consectetuer tincidunt. Vivamus risus urna, dignissim non, tempor sed, malesuada vel, libero. Aenean placerat. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Ut a eros. Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Curabitur mauris quam, lacinia ac, varius id, elementum vitae, quam. Quisque mattis pharetra neque. Integer lorem. Donec id nulla nec dolor mattis hendrerit. Curabitur libero. Suspendisse a augue. Donec id enim et nisl blandit accumsan. Fusce sit amet augue. Suspendisse tristique vulputate risus. Aliquam sapien. Maecenas adipiscing. Donec eget massa.</p>

		<ul class = 'news_page_text_list'>
				<li><a href = '/pdfs/LCA09Release.pdf'>LCA 2009 Press Release</a></li>
				<li><a href = '/pdfs/LCA09Bid.pdf'>LCA 2009 Bid Document</a></li>
				<li><a href = '/pdfs/Ghosts_Meeting_in_Hobart.pdf'>Ghosts Meeting in Hobart Press Release</a></li>
		</ul>

<%init>
featured = []
count = 0
limit = 4
for d in c.db_content_news:
    if (h.featured_image(d.title) is not False) and (count < limit):
        featured.append(d)
        count += 1
    
</%init>

<%method big_promotion>
%for d in c.db_content_news:
%    directory = h.featured_image(d.title, big = True)
%    if directory is not False:
			<div class = 'news_banner'>
				<div class = 'news_banner_left'>
					<img src = '<% directory %>/1.png' alt="<% d.title %>" title="<% d.title %>">
				</div>
				<div class = 'news_banner_right'>
					<img src = '<% directory %>/3.png' alt="<% d.title %>" title="<% d.title %>">
				</div>
				<a href = '/media/news/<% d.id %>'>
				<img src = '<% directory %>/2.png' alt="<% d.title %>" title="<% d.title %>">
				</a>
			</div>
%    #endif
%#endfor
</%method>

<%method extra_head>
%for d in c.db_content_news:
%    directory = h.featured_image(d.title, big = True)
%    if directory is not False:
<style type="text/css">
.content
{
    background-image: url(images/content_bg_tall.png);
}
</style>
%        break
%    #endif
%#endfor
</%method>
