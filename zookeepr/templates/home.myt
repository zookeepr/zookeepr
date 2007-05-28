<h1 class="pop">Australia's annual linux conference is fun, informal and seriously technical.</h1>

<p>In 2008, linux.conf.au returns to Melbourne &ndash; one of the world's best technical conferences, in one of the world's most liveable cities. The MEL<span class="eight">8</span>OURNE team plans on making our guests feel at home and the locals proud.</p>

<h2>When</h2>
<p>linux.conf.au opens on Wednesday January 30th and concludes with an Open Day on February 2nd 2008. Special interest <a href="/mini-confs">mini-confs</a> are held before the conference on Monday and Tuesday.</p>

<h2>Where</h2>
<p>In 2008, the <a href="http://www.unimelb.edu.au">University of Melbourne</a> plays host to linux.conf.au.</p>

<!-- 

<p>Organised and run entirely by volunteers: people who've been there and done that in the <strong>Australian Free and Open Source Software community</strong>. Each year, many more papers, proposals and submissions are received than can possibly be scheduled in the program.</p>

<p>The hard choices are made, a program is scheduled and the organising team slaves to put on the best conference they possibly can. The pressure is intense because expectations are high.</p>

<p>linux.conf.au is made possible by the generous contributions of our sponsors, speakers, delegates and volunteers.</p>

-->

<p>linux.conf.au 2008 in Mel<span class="eight">8</span>ourne, Victoria - The place to be.</p>

<h2>Mini-confs</h2>

<p>The call for <a href="/mini-confs">mini-conf proposals</a> is now open. If you have a mini-conf 
you would like to run, please let us know.</p>

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
