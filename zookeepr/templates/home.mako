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
<p>Subscribe to our <a href="/media/news/rss">news feed</a> to stay up to date with announcements, as we prepare to host the best <a href="about/linux.conf.au">linux.conf.au</a> yet!</p>

<h1>linux.conf.au 2010 Current Happenings</h1>

<h2>Registrations are now open!</h2>

<p>Early Bird Registrations for LCA2010 have sold out! If you haven't already registered, you still have a chance. <a href="/register/status">Registrations</a> will remain open until 24 December 2009. So get in quick!!</p>

<table>
<tr class="even">
<td><b>Registrations Opened</b></td> <td>10 October 2009</td> 
</tr>

<tr class="odd">
<td><b>Early Birds Sold Out</b></td> <td><s>13</s> 5 November 2009</td> 
</tr>

<tr class="even">
<td><b>Registrations Closes</b></td> <td>24 December 2009</td> 
</tr>
</table>

<p>To register for linux.conf.au 2010, please go to the <a href="/register/status">Registration Page</a> or simply click on the Register link in the toolbox.</p>


<h2>Funding</h2>

<p>There are three LCA2010 Funding Programmes available for those highly regarded people out there who contribute in important ways to the free and open source community and whom, without financial assistance, would not be able to attend LCA2010.</p>

<h3>Winners of the Funding Programmes</h3>

<h5>InternetNZ Oceania Programme</h5>

<table>
<tr class="odd">
<td>Etuate Cocker</td>
</tr>

<tr class="even">
<td>Andy Fitzsimon</td>
</tr>

<tr class="odd">
<td>Opetaia Simati</td> 
</tr>

<tr class="even">
<td>Bernard Ugalde</td> 
</tr>
</table>

<h5>InternetNZ Kiwi Fellowship</h5>

<table>
<tr class="odd">
<td>Mark Osborne</td>
</tr>

<tr class="even">
<td>Lynne Pope</td>
</tr>

<tr class="odd">
<td>Nicolas Steenhout</td> 
</tr>
</table>

<h5>Google Diversity Programme</h5>

<table>
<tr class="odd">
<td>Sara Falamaki</td>
</tr>

<tr class="even">
<td>Elizabeth Garbee</td> 
</tr>

<tr class="odd">
<td>Liz Henry</td>
</tr>

<tr class="even">
<td>Emma Jane Hogbin</td>
</tr>

<tr class="odd">
<td>Nancy Mauro-Flude</td>
</tr>

</table>

<p>Watch this space, sign up for the <a href="http://lists.linux.org.au/listinfo/announce">mailing list</a>, follow us on <a href="http://twitter.com/linuxconfau">Twitter</a>/<a href="http://identi.ca/group/lca2010">Identica</a> or grab the <a href="http://www.lca2010.org.nz/media/news/rss">RSS feed</a>!</p>


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
