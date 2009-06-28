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

		<h1>linux.conf.au 2010 in Wellington, New Zealand!</h1>

		<p>linux.conf.au is one of the world's best conferences for free and open source software!</p>
		<p>Now in its <a href="/about/history">11th year</a>, linux.conf.au attracts some of the brightest minds from the southern and northern hemisphere – a major annual event in the conference calendar.</p>
		<p>LCA2010 will be held from Monday 18 January to Friday 23 January 2010 at the <a href="/about/venue">Wellington Convention Centre</a> in <a href="/wellington/about">Wellington</a>, <a href="/about/new_zealand">New Zealand</a>, home of the little blue penguin or Kororā as they are called in Māori, New Zealand's indigenous language. What better place to bring the world's biggest gathering of Linux enthusiasts?</p>
		<p><a href="/about/linux.conf.au">linux.conf.au</a> is run by the community, for the community – much in the same way that the community has made <a href="/about/linux_open_source">Linux</a>, and the whole <a href="/about/linux_open_source">free and open source</a> movement the phenomenon it is today.</p>
		<p>Subscribe to our <a href="/media/news/rss">news feed</a> to stay up to date with announcements, as we prepare to host the best <a href="http://linux.conf.au/">linux.conf.au</a> yet!</p>


<%def name="big_promotion()">
% for d in c.db_content_news_all:
     <% directory = h.featured_image(d.title, big = True) %>
%    if directory is not False:
			<div class = 'news_banner'>
%      if h.os.path.isfile(directory + "/1.png"):
				<div class = 'news_banner_left'>
					<a href = '/media/news/${ d.id }'><img src = '${ directory }/1.png' alt="${ d.title }" title="${ d.title }"></a>
				</div>
%      endif
%      if h.os.path.isfile(directory + "/3.png"):
				<div class = 'news_banner_right'>
					<a href = '/media/news/${ d.id }'><img src = '${ directory }/3.png' alt="${ d.title }" title="${ d.title }"></a>
				</div>
%      endif
				<a href = '/media/news/${ d.id }'>
					<img src = '${ directory }/2.png' alt="${ d.title }" title="${ d.title }">
				</a>
			</div>
  <br /><br />
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
