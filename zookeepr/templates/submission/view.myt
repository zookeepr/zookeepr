<h2 id="title"><% c.submission.title | h %></h2>

<p>
Submitted by
% if c.person and (c.person == c.submission.person):
you!
% else:
<% c.submission.person.email_address %>
% #endif
</p>

<p id="submission_type">
(<% c.submission.submission_type.name | h %>)
</p>

<p id="abstract">
<% c.submission.abstract | h %>
</p>

<p id="experience">
<% c.submission.experience | h %><br />
</p>

<p>
<b>URL:</b><% h.link_to(c.submission.url) %>
</p>

<hr />

<p id="actions">
% if c.can_edit:
<% h.link_to('Edit', url=h.url(action='edit',id=c.submission.id)) %> |
% #end if
<% h.link_to('Back', url=h.url(action='index')) %>
</p>
