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

<h3>Registrations are now open!</h3>

<p>Online <a href="/register/status">registrations</a> for LCA2010 are now open! There are only a limited number of Early Bird Registrations available. Early Bird tickets will be available until 13 November 2009, unless sold out earlier. So get in quick!!</p>

<table>
<tr class="even">
<td><b>Registrations Opened</b></td> <td>10 October 2009</td> 
</tr>

<tr class="odd">
<td><b>Early Bird Closes</b></td> <td>13 November 2009</td> 
</tr>

<tr class="even">
<td><b>Registrations Closes</b></td> <td>24 December 2009</td> 
</tr>
</table>

<p>To register for linux.conf.au 2010, please go to the <a href="/register/status">Registration Page</a> or simply click on the Register link in the toolbox.</p>


<h2>LCA2010 Miniconfs</h2>

<br />
<p>The <a href="/programme/miniconfs">linux.conf.au 2010 Miniconfs</a> have put put their
<a href="/media/news/92">Call for Miniconf Papers</a>!</p>

<table>
  <tr class="odd">
    <td><a href="http://www.lca2010.org.nz/wiki/Miniconfs/Arduino">Arduino</a></td>  <td>Jonathan Oxer</td>
    <td><a href="http://www.lca2010.org.nz/wiki/Miniconfs/Arduino">Submit a proposal</a></td>
  </tr>
  <tr class="even">
    <td><a href="http://www.lca2010.org.nz/wiki/Miniconfs/Business_of_Open_Source">Business of Open Source</a></td>  <td>Martin Michlmayr</td>
    <td><a href="https://fossbazaar.org/content/lca-devbiz-january-2010">Submit a proposal</a></td>
  </tr>
  <tr class="odd">
    <td><a href="http://www.lca2010.org.nz/wiki/Miniconfs/Data_Storage_and_Retrieval">Data Storage and Retrieval</a></td>  <td>Peter Lieverdink</td>
    <td><a href="http://miniconf.osda.asn.au/node/add/proposal">Submit a proposal</a></td>
  </tr>
  <tr class="even">
    <td><a href="http://www.lca2010.org.nz/wiki/Miniconfs/Distro_Summit">Distro Summit</a></td>  <td>Fabio Tranchitella</td>
    <td><a href="http://distrosummit.org/cfp.html">Submit a proposal</a></td>
  </tr>
  <tr class="odd">
    <td><a href="http://www.lca2010.org.nz/wiki/Miniconfs/Education">Education</a></td>  <td>Tabitha Roder</td>
    <td><a href="http://laptop.org.nz/node/add/miniconfsubmission">Submit a proposal</a></td>
  </tr>
  <tr class="even">
    <td><a href="http://www.lca2010.org.nz/wiki/Miniconfs/Free_The_Cloud%21">Free The Cloud!</a></td>  <td>Evan Prodromou</td>
    <td><a href="http://www.lca2010.org.nz/wiki/Miniconfs/Free_The_Cloud%21">Submit a proposal</a></td>
  </tr>
  <tr class="odd">
    <td><a href="http://www.lca2010.org.nz/wiki/Miniconfs/Haecksen_and_Linuxchix">Haecksen and Linuxchix</a></td>  <td>Joh Clarke</td>
    <td><a href="http://haecksen.org.nz/node/add/miniconfsubmission">Submit a proposal</a></td>
  </tr>
  <tr class="even">
    <td><a href="http://www.lca2010.org.nz/wiki/Miniconfs/Libre Graphics Day">Libre Graphics Day</a></td>  <td>Jon Cruz</td>
    <td><a href="http://libregraphicsday.org/submit-proposal">Submit a proposal</a></td>
  </tr>
  <tr class="odd">
    <td><a href="http://www.lca2010.org.nz/wiki/Miniconfs/Multicore_and_Parallel_Computing">Multicore and Parallel Computing</a></td>  <td>Nicol&aacute;s Erd&ouml;dy</td>
    <td><a href="http://multicorenz.wordpress.com/lca2010-miniconf/">Submit a proposal</a></td>
  </tr>
  <tr class="even">
    <td><a href="http://www.lca2010.org.nz/wiki/Miniconfs/Multimedia">Multimedia</a></td>  <td>Conrad Parker</td>
    <td><a href="http://www.lca2010.org.nz/wiki/Miniconfs/Multimedia">Submit a proposal</a></td>
  </tr>
  <tr class="odd">
    <td><a href="http://www.lca2010.org.nz/wiki/Miniconfs/Open_and_the_Public_Sector">Open and the Public Sector</a></td>  <td>Daniel Spector</td>
    <td><a href="http://open.org.nz/lca2010-open-government-miniconf/">Submit a proposal</a></td>
  </tr>
  <tr class="even">
    <td><a href="http://www.lca2010.org.nz/wiki/Miniconfs/Open_Programming_Languages">Open Programming Languages</a></td>  <td>Christopher Neugebauer</td>
    <td><a href="http://blogs.tucs.org.au/oplm/cfp/">Submit a proposal</a></td>
  </tr>
  <tr class="odd">
    <td><a href="http://www.lca2010.org.nz/wiki/Miniconfs/System_Administration">System Administration</a></td>  <td>Simon Lyall</td>
    <td><a href="http://sysadmin.miniconf.org/cfp10.html">Submit a proposal</a></td>
  </tr>
  <tr class="even">
    <td><a href="http://www.lca2010.org.nz/wiki/Miniconfs/Wave_Developers">Wave Developers</a></td>  <td>Shane Stephens</td>
    <td><a href="http://sites.google.com/site/waveminiconfatlca/signup-form">Submit a proposal</a></td>
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
