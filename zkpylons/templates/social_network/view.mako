<%inherit file="/base.mako" />

<h2>View Social Network</h2>

<table>
  <tr class="odd">
    <td><b>Name:</b></td><td>${ c.social_network.name  }</td>
  </tr>
  <tr class="even">
    <td valign="top"><b>Logo:</b></td><td>
      <img style="padding-right: 5px" src="/images/${ c.social_network.logo }">
      ${ c.social_network.logo }
    </td>
  </tr>
  <tr class="odd">
    <td valign="top"><b>URL:</b></td><td>${ c.social_network.url }</td>
  </tr>
</table>

<h3>Members</h3>

<table>
% if len(c.social_network.people) > 0:
  <tr>
    <th>Name</th>
    <th>Username</th>
  </tr>
  %   for person in sorted(c.social_network.people, key=lambda p: p.id):
  <tr>
    <td>${ h.link_to(person.fullname, url=h.url_for(controller='person', action='view', id=person.id)) }</td>
    <td>${ c.social_network.people[person] }</td>
  </tr>
%   endfor
% else:
  <tr>
    <td>No members</td>
  </tr>
% endif
</table>


    <p>
    ${ h.link_to('Edit', url=h.url_for(action='edit',id=c.social_network.id)) } |
    ${ h.link_to('Delete', url=h.url_for(action='delete',id=c.social_network.id)) } |
    ${ h.link_to('Back', url=h.url_for(action='index', id=None)) }</p>

<%def name="title()">
Social Network -
${ c.social_network.name } -
View -
 ${ parent.title() }
</%def>
