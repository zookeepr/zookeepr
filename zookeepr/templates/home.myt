<h1 class="pop">Australia's annual linux conference is fun, informal and seriously technical.</h1>

<p>In 2008, linux.conf.au returns to Melbourne. It is one of the 
world's best linux conferences. The MEL<span class="eight">8</span>OURNE 
team plans on making our guests feel at home and the locals proud.</p>

<div id="column-container" style="margin:0 auto;">

<div id="hp-announce">
<h2>Call for Presentations</h2>

<p>The <a href="/presentations">Call for Presentations</a> (aka <a
href="/presentations">Call for Papers</a>) is now open. If you have a talk or
a tutorial you would like to present, please let us know. Read the <a href="/presentations/announcement">full announcement</a>.</p>

</div>

<div id="hp-news">

<h2>News</h2>

<ul class="hp-list" style="margin: 0px; padding: 0px;">
<li><a href="/2008/sponsors-media/news/keynote-secured">linux.conf.au 2008 - Keynote Secured</a><br />2 July 2007</li>
<li><a href="/mini-confs">Mini-conf proposal submissions open</a><br />15 June 2006</li>
</ul>

</div>
</div>

<div id="rest" style="clear: both;">

<h2>When</h2>
<p>linux.conf.au opens on Wednesday January 30th and concludes with an Open Day on February 2nd 2008. Special interest <a href="/mini-confs">mini-confs</a> are held before the conference on Monday and Tuesday.</p>

<h2>Where</h2>
<p>In 2008, the <a href="http://www.unimelb.edu.au">University of Melbourne</a> plays host to linux.conf.au.</p>

<p>linux.conf.au 2008 in Mel<span class="eight">8</span>ourne, Victoria - The place to be.</p>

</div>

<!--
FIXME: Dirty hack so all the tests don't fail
% if c.signed_in_person:
<div id="proposals">

<p>You've submitted the following proposals to the CFP:
<ul>

% for s in c.signed_in_person.proposals:

# FIXME: dirty hack
%	if c.signed_in_person in s.people:
<li>
<% h.link_to(s.title, url=h.url(controller='proposal', action='view', id=s.id)) %>

<span class="actions">
[
<% h.link_to('edit', url=h.url(controller='proposal', action='edit', id=s.id)) %>
|
<% h.link_to('delete', url=h.url(controller='proposal', action='delete', id=s.id)) %>
]
</span>

</li>
% #endif
% #endfor

</ul>

</p>

<p>
<% h.link_to('submit another', url=h.url(controller='proposal', action='new')) %>
</p>

</div>

## reviewer block
% if 'reviewer' in [r.name for r in c.signed_in_person.roles]:
<div id="reviewer">
<p>
You're a reviewer!  You can <% h.link_to("review stuff!", url=h.url(controller='proposal', action='index')) %>
</p>
</div>
% #endif

% #endif c.signed_in_person
-->
