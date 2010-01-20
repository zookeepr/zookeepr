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
<p>LCA2010 will be held from Monday 18 January to Saturday 23 January 2010 at the <a href="/about/venue">Wellington Convention Centre</a> in <a href="/wellington/about">Wellington</a>, <a href="/about/new_zealand">New Zealand</a>, home of the little blue penguin or Kororā as they are called in Māori, New Zealand's indigenous language. What better place to bring the world's biggest gathering of Linux enthusiasts?</p>
<p>Watch this space, sign up for the <a href="http://lists.linux.org.au/listinfo/announce">mailing list</a>, follow us on <a href="http://twitter.com/linuxconfau">Twitter</a>/<a href="http://identi.ca/group/lca2010">Identica</a> or grab the <a href="http://www.lca2010.org.nz/media/news/rss">RSS feed</a>!</p>

<h1>linux.conf.au 2010 Current Happenings</h1>

<p>See the <a href="/schedule">programme schedule</a>.</p>

<h1>Life Flight Trust Charity Fundraiser - Donate Now!</h1>

<p>LCA2010 delegates are invited to make donations to the Life Flight Trust and be in to win an exclusive once-in-a-lifetime experience on Saturday 23rd January 2010. The highest donor/s will win the grand prize - a trip for four people as honorary crew-members on a helicopter winch training mission!</p>

<p>Delegates can donate as an individual and elect three friends of your choice to come along on this ride, OR enter as four people donating under one group name. Donations are accepted up until Friday 6pm, and the winner will be announced at the Penguin Dinner on Friday night.</p>

<h2><a href="http://www.fundraiseonline.co.nz/LCA2010/">Donate here</a></h2>

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
