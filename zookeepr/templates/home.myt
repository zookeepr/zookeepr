<h1>Australia's annual linux conference is fun, informal and seriously technical.</h1>

<p>Organised and run entirely by volunteers, linux.conf.au is put together by a new team each year. A call for papers and participation is put out, and many more submissions are received than can possibly be scheduled in the program.</p>
<p>linux.conf.au has a papers committee, made up of people who've been there and done that in the <strong>Australian Free and Open Source Software community</strong>.</p>
<p>Hard choices are made, a program is scheduled, and the organising team slaves to put on the best conference they possibly can. The pressure is intense because the expectations are high.</p>
<p>linux.conf.au is only made possible by the generous contributions of our sponsors, speakers, delegates and volunteers.</p>

<h2>It is brilliant. Be there.</h2>
<p>In 2008, linux.conf.au returns to Melbourne. One of the world's best technical conferences, in one of the world's most liveable cities. The MEL<span class="eight">8</span>OURNE team plans on making guests feel at home, and locals proud.</p>
<p>The previous linux.conf.au was held in Sydney - see <a href="http://lca2007.linux.org.au/">http://lca2007.linux.org.au/</a> for all the details, including videos of most of the conference sessions.</p>

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
