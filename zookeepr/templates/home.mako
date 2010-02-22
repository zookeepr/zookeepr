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
<p>LCA2010 was held from Monday 18 January to Saturday 23 January 2010 at the <a href="/about/venue">Wellington Convention Centre</a> in <a href="/wellington/about">Wellington</a>, <a href="/about/new_zealand">New Zealand</a>, home of the little blue penguin or Kororā as they are called in Māori, New Zealand's indigenous language. What better place to bring the world's biggest gathering of Linux enthusiasts?</p>
<p>Watch this space, sign up for the <a href="http://lists.linux.org.au/listinfo/announce">mailing list</a>, follow us on <a href="http://twitter.com/linuxconfau">Twitter</a>/<a href="http://identi.ca/group/lca2010">Identica</a> or grab the <a href="http://www.lca2010.org.nz/media/news/rss">RSS feed</a>!</p>

<h1>Can't get enough linux.conf.au?</h1>

<p>We're all sad that linux.conf.au is over for another year.  But the good news is that you only have to wait until 2011 for the <b>next</b> linux.conf.au!  So stop Following the Signs to Wellington, and now <a href="http://followtheflow.org/">Follow the Flow</a> to Brisbane!</p>

<h1>Videos of LCA2010</h1>

<p>Didn't see all the talks that you wanted to see?  Check out the videos for LCA2010 which will be available late February/early March so watch this space.</p>

<h1>Over $33,000 raised in support of Life Flight Trust!</h1>

<p>As supporters of Life Flight Trust, linux.conf.au 2010 raised over $33,000 in support of a national air ambulance service! The delegates in support of a group called the Wenches for Winching donated the most amount of money to Life Flight Trust, and won a unique, adrenlin-packed experience: A trip for four as honorary crew-members on a helicopter winch training mission, where they wil be winched down from the helicopter to the ground and up again on an 8mm steel cable!  Theodore T'so, as the individual who donated the most amount of money to Life Flight Trust, won a framed full-colour aerial photograph of Wellington city, shot by, Crew Chief, Dave Greenberg from the Westpac Rescue Helicopter.</p>

<h2>You can still <a href="http://www.fundraiseonline.co.nz/LCA2010/">donate here</a></h2>

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
