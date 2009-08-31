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

<h2>LCA2010 Miniconfs</h2>

<br />
<p>LCA2010 Organisers have <a href="/media/news/74">announced</a> the
successful <a href="/programme/miniconfs">Miniconfs for LCA2010</a>:</p>

<table>
  <tr class="odd">
    <td><b>Arduino</b></td>  <td>Jonathan Oxer</td>
  </tr>
  <tr class="even">
    <td><b>Business of Open Source</b></td>  <td>Martin Michlmayr</td>
  </tr>
  <tr class="odd">
    <td><b>Data Storage and Retrieval</b></td>  <td>Peter Lieverdink</td>
  </tr>
  <tr class="even">
    <td><b>Distro Summit</b></td>  <td>Fabio Tranchitella</td>
  </tr>
  <tr class="odd">
    <td><b>Education</b></td>  <td>Tabitha Roder</td>
  </tr>
  <tr class="even">
    <td><b>Free The Cloud!</b></td>  <td>Evan Prodromou</td>
  </tr>
  <tr class="odd">
    <td><b>Haecksen and Linuxchix</b></td>  <td>Joh Clarke</td>
  </tr>
  <tr class="even">
    <td><b>Libre Graphics Day</b></td>  <td>Jon Cruz</td>
  </tr>
  <tr class="odd">
    <td><b>Multicore and Parallel Computing</b></td>  <td>Nicolas Erdody</td>
  </tr>
  <tr class="even">
    <td><b>Multimedia</b></td>  <td>Conrad Parker</td>
  </tr>
  <tr class="odd">
    <td><b>Open and the Public Sector</b></td>  <td>Daniel Spector</td>
  </tr>
  <tr class="even">
    <td><b>Open Programming Languages</b></td>  <td>Christopher Neugebauer</td>
  </tr>
  <tr class="odd">
    <td><b>System Administration</b></td>  <td>Simon Lyall</td>
  </tr>
  <tr class="even">
    <td><b>Wave Developers</b></td>  <td>Shane Stephens</td>
  </tr>
</table>

<h2>Registrations coming soon!</h2>

<p>Online registrations for LCA2010 will be opening in September 2009. There will be a limited number of Early Bird Registrations available, so get in early.</p>

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
