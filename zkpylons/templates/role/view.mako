<%inherit file="/base.mako" />
<h1>View Role</h1>

<table>
  <tr class="odd">
    <td>Name:</td>
    <td>${ c.role.name }</td>
  </tr>
  <tr class="even">
    <td>Pretty Name:</td>
    <td>${ c.role.pretty_name }</td>
  </tr>
  <tr class="odd">
    <td>Comment:</td>
    <td>${ c.role.comment }</td>
  </tr>
  <tr class="even">
    <td>Display Order:</td>
    <td>${ c.role.display_order }</td>
  </tr>
</table>

<h2>People with this role</h2>

% if len(c.role.people) > 0:
<table>
%   for person in c.role.people:
<tr class="${ h.cycle('even', 'odd') }">
<td>
${ h.link_to("%d - %s %s" % (person.id, person.firstname, person.lastname), url=h.url_for(controller='person', id=person.id, action='view')) }
</td>
<td>
${ h.link_to("roles", url=h.url_for(controller='person', id=person.id, action='roles')) }
<td>
%   endfor
</table>
% else:
<p>None</p>
% endif

<hr>
<p>
<ul>
  <li>${ h.link_to('Edit', url=h.url_for(action='edit',id=c.role.id)) }</li>
  <li>${ h.link_to('Back', url=h.url_for(action='index', id=None)) }</li>
</ul>
</p>
