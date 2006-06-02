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

<h2>submissions</h2>

<table>

% for s in c.person.submissions:
<tr>
<td><% h.link_to(s.title, h.url_for(controller='/submission', action='view', id=s.id)) %></td>
<td><% s.abstract %></td>
<td>
%	if s.submission_type:
<% s.submission_type.name %>
%
</td>
<td>
% 	if s.attachment:
has attachment
%
</td>
% #endfor
</table>

<hr />

% if c.can_edit:
<% h.link_to('Edit', url=h.url(action='edit',id=c.person.handle)) %> |
% #end if
<% h.link_to('Back', url=h.url(action='index')) %>
