<%inherit file="/base.mako" />
<%
featured = []
count = 0
limit = 4
for d in c.db_content_news_all:
    if (h.featured_image(d.title) is not False) and (count < limit):
        featured.append(d)
        count += 1
%>


## -- coding: utf-8 --
		<!-- <img src = '/images/heightfix.png' class = 'heightfix' alt = ''> -->

		<img src="images/banner.gif" style="border: 0" alt="Follow the signs!" /><br /><br />
		<h1>linux.conf.au 2010 in Wellington, New Zealand!</h1>

		<p>linux.conf.au is one of the world's best conferences for free and open source software!</p>
		<p>Now in its 11th year, linux.conf.au attracts some of the brightest minds from the southern and northern hemisphere – a major annual event in the conference calendar.</p>
		<p>In January 2010 from the 18th till the 23rd, linux.conf.au will be visiting Wellington, New Zealand, home of the little blue penguin or Kororā as they are called in Māori, New Zealand's indigenous language. What better place to bring the world's biggest gathering of Linux enthusiasts?</p>
		<p>linux.conf.au is run by the community, for the community – much in the same way that the community has made Linux, and the whole free and open source movement the phenomenon it is today.</p>
		<p>Subscribe to our <a href="/media/news/rss">news feed</a> to stay up to date with announcements, as we prepare to host the best <a href="http://linux.conf.au/">linux.conf.au</a> yet!</p>


<%def name="big_promotion()">
% for d in c.db_content_news_all:
     ${ directory = h.featured_image(d.title, big = True) }
%    if directory is not False:
			<div class = 'news_banner'>
				<div class = 'news_banner_left'>
					<a href = '/media/news/${ d.id }'><img src = '${ directory }/1.png' alt="${ d.title }" title="${ d.title }"></a>
				</div>
				<div class = 'news_banner_right'>
					<a href = '/media/news/${ d.id }'><img src = '${ directory }/3.png' alt="${ d.title }" title="${ d.title }"></a>
				</div>
				<a href = '/media/news/${ d.id }'>
					<img src = '${ directory }/2.png' alt="${ d.title }" title="${ d.title }">
				</a>
			</div>
        <% break %>
%    endif
% endfor
</%def>

<%def name="extra_head()">
%for d in c.db_content_news_all:
     <% directory = h.featured_image(d.title, big = True) %>
%    if directory is not False:
<style type="text/css">
.content
{
    background-image: url(/images/content_bg_tall.png);
}
</style>
        <% break %>
%    endif
% endfor
</%def>
