<h1>View submission</h1>

<p>
   <b>Title:</b>
    <% c.submission.title | h %><br />
</p>

<p>
   <b>Type:</b>
    <% c.submission.submission_type | h %><br />
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

% h.log(c.submission.person)

% if c.submission.person:
<p>
<b>Person:</b>
<% h.link_to(c.submission.person.handle, url=h.url(controller='person', action='view', id=c.submission.person.handle)) %>
</p>
% #endif

<hr />

% if c.can_edit:
<% h.link_to('Edit', url=h.url(action='edit',id=c.submission.id)) %> |
% #end if
<% h.link_to('Back', url=h.url(action='index')) %>
