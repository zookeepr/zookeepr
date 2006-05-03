<h1>View person</h1>

<p>
   <b>handle:</b>
    <% c.person.handle | h %><br />
</p>

<p>
   <b>Email:</b>
    <% c.person.email_address | h %><br />
</p>

<p>
   <b>First name:</b>
    <% c.person.firstname | h %><br />
</p>

<p>
   <b>Last name:</b>
    <% c.person.lastname | h %><br />
</p>

<p>
   <b>Phone:</b>
<% c.person.phone %><br />
</p>

<p>
<b>Fax:</b>
<% c.person.fax %>
</p>

<hr />

% if c.can_edit:
<% h.link_to('Edit', url=h.url(action='edit',id=c.person.handle)) %> |
% #end if
<% h.link_to('Back', url=h.url(action='index')) %>
