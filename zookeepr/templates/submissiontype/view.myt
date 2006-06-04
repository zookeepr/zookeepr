<h2>View submission type</h2>

<p>
   <b>Name:</b>
    <% c.submissiontype.name | h %><br />
</p>

% if c.can_edit:
<% h.link_to('Edit', url=h.url(action='edit',id=c.submissiontype.id)) %> |
% #end if
<% h.link_to('Back', url=h.url(action='index', id=None)) %>
