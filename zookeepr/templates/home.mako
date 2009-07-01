## -- coding: utf-8 --
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


<!-- <img src = '/images/heightfix.png' class = 'heightfix' alt = ''> -->

<h1>linux.conf.au 2010 in Wellington, New Zealand!</h1>

<p>linux.conf.au is one of the world's best conferences for free and open source software!</p>
<p>LCA2010 will be held from Monday 18 January to Friday 23 January 2010 at the <a href="/about/venue">Wellington Convention Centre</a> in <a href="/wellington/about">Wellington</a>, <a href="/about/new_zealand">New Zealand</a>, home of the little blue penguin or Kororā as they are called in Māori, New Zealand's indigenous language. What better place to bring the world's biggest gathering of Linux enthusiasts?</p>
<p>Subscribe to our <a href="/media/news/rss">news feed</a> to stay up to date with announcements, as we prepare to host the best <a href="about/linux.conf.au">linux.conf.au</a> yet!</p>

<h1>linux.conf.au 2010 Current Happenings</h1>

<h2>Call for Papers</h2>
<p>Monday 29 June 2009 – Call for Papers are now open! The LCA2010 Papers Committee is looking for a broad range of papers spanning everything from programming and software to desktop and userspace to community, government and education.  
If you would like to take this opportunity to submit a Paper to LCA2010, please visit <a href="programme/papers_info">Papers Info</a> for more information before <a href="programme/submit_a_paper">Submitting a Paper</a>.</p>

<table>
<tr class="odd">
  <td>Call for Papers opens</td><td>Monday 29 June 2009</td>
</tr>
<tr class="even">
  <td>Call for Papers closes</td><td>Friday 24 July 2009</td>
</tr>
<tr class="odd">
  <td>Papers Notifcations</td><td>Early September 2009</td>
</tr>
</table>

<h2>Call for Miniconfs</h2>

<p>Monday 15 June 2009 – Call for Miniconfs are now open!. LCA2010 provides the opportunity of hosting 1-day mini-conferences on a variety of Free Software related subjects; from Linux and the BSDs to OpenOffice.org, from networking to audio-visual magic, from deep hacks to Creative Commons.  
If you would like to take this opportunity to submit a Miniconf to LCA2010, please visit <a href="programme/miniconf_info">Miniconf Info</a> for more information before <a href="programme/submit_a_miniconf">Submitting a Miniconf</a>.</p>

<table>
<tr class="odd">
  <td>Call for Miniconfs opens</td><td>Monday 15 June 2009</td>
</tr>
<tr class="even">
  <td>Call for Miniconfs closes</td><td>Friday 17 July 2009</td>
</tr>
<tr class="odd">
  <td>Miniconf Notifications</td><td>Early September 2009</td>
</tr>
</table>


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

<%def name="short_title()"><%
  return "Homepage"
%></%def>
