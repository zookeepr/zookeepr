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

                                            <h2 class="netv-postheader">
                              <img src="images/postheadericon.png" width="26" height="26" alt="postheadericon" />
                              Welcome to linux.conf.au 2011!</h2>


<p>linux.conf.au is one of the world's best conferences for free and open source software. In 2011 lca is going
to be held in Brisbane at QUT Gardens Point. </p>

<h3> Call for Papers, Miniconfs, Posters and Tutorials are now open </h3>

<p>The linux.conf.au 2011 papers team now welcomes proposals of papers from all areas of the open source community, until Saturday 7th August 2010. In early September 2010, successful proposals will be notified.</p>

<p>The papers submissions must be of the following types:</p>

<table>
<tr class="odd">
  <td>Presentations</td><td>45 minutes</td>
</tr>
<tr class="even">
  <td>Tutorials</td><td>1 hour and 45 minutes (short)</td>
</tr>
<tr class="odd">
  <td>Tutorials</td><td>3 hours and 30 minutes (long)</td>
</tr>
<tr class="even">
  <td>Posters</td><td><a href="/programme/posters">Poster information<a></td>
</tr>
</table>

<p>Presentation times include time for questions. For more information on the call for papers please refer to the respective headings under the <a href="/programme/about">Programme Menu</a></p>

<p>If you wish to submit a proposal for a one-day community organised mini-conference, see <a href="/programme/miniconfs">Miniconf Information</a>.</p>

<a name="ImportantDates"></a><h3>Important Dates</h3>

<table>
<tr class="odd">
  <td>Call for Papers opens</td><td>Tuesday 13th July 2010</td>
</tr>
<tr class="even">
  <td>Call for Papers closes</td><td>Saturday 7th August 2010 </td>

</tr>
<tr class="odd">
  <td>Email Notifications from<br />Papers Committee</td><td>Early September 2010</td>
</tr>
<tr class="even">
  <td>Conference begins</td><td>Monday 24th January 2011</td>
</tr>
</table>

<%def name="short_title()"><%
  return "Homepage"
%></%def>
