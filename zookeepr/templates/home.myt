<h1>Test Setup</h1>

<p> <a href="/programme/submit_a_presentation">Call for Presentations</a> </p>

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
