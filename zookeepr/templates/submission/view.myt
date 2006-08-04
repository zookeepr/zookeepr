<h2>View submission</h2>

<p>
   <b>Title:</b>
    <% c.submission.title | h %><br />
</p>

<p>
   <b>Type:</b>
    <% c.submission.submission_type.name | h %><br />
</p>

<p>
   <b>abstract:</b>
    <% c.submission.abstract | h %><br />
</p>

<p>
   <b>Experience:</b>
    <% c.submission.experience | h %><br />
</p>

<p>
   <b>URL:</b>
<% h.link_to(c.submission.url) %><br />
</p>

% if c.submission.person:
<p>
<b>Person:</b>
<% h.link_to(c.submission.person.email_address, url=h.url(controller='person', action='view', id=c.submission.person.id)) %>
</p>
% #endif

<hr />

% if c.can_edit:
<% h.link_to('Edit', url=h.url(action='edit',id=c.submission.id)) %> |
% #end if
<% h.link_to('Back', url=h.url(action='index')) %>
