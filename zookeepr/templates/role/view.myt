<h1>View proposal type</h1>

<p>
   <b>Name:</b>
    <% c.role.name | h %><br>
</p>

<p>
% if c.can_edit:
<% h.link_to('Edit', url=h.url(action='edit',id=c.role.id)) %> |
% #end if
<% h.link_to('Back', url=h.url(action='index', id=None)) %></p>
