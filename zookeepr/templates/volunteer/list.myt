    <h2>List of Volunteers</h2>
% if len(c.volunteer_collection) > 0:

    <table>
      <tr>
        <th>Volunteer</th>
        <th>Registration</th>
        <th>Name</th>
        <th>Phone Number</th>
        <th>Accepted</th>
        <th>&nbsp;</th>
        <th>&nbsp;</th>
        <th>&nbsp;</th>
      </tr>
%   for volunteer in c.volunteer_collection:
      <tr>
        <td><% h.link_to('id: ' + str(volunteer.id), url=h.url(action='view', id=volunteer.id)) %></td>
%       if volunteer.person.registration:
        <td><% h.link_to('id: ' + str(volunteer.person.registration.id), url=h.url(controller='registration', action='view', id=volunteer.person.registration.id)) %></td>
%       else:
        <td></td>
%       #endif
        <td><% h.link_to(m.apply_escapes(volunteer.person.firstname + ' ' + volunteer.person.lastname, 'h'), h.url(controller='person', action='view', id=volunteer.person.id)) %></td>
        <td><% volunteer.person.mobile or volunteer.person.phone | h %></td>
        <td><% h.yesno(volunteer.accepted) %></td>
%       if volunteer.accepted:
        <td><% h.link_to('reject', url=h.url(action='reject', id=volunteer.id)) %></td>
%       else:
        <td><% h.link_to('accept', url=h.url(action='accept', id=volunteer.id)) %></td>
%       #endif
%       if c.can_edit:
%           for action in ['edit', 'delete']:
        <td><% h.link_to(action, url=h.url(action=action, id=volunteer.id)) %></td>
%           #endfor
%       #endif
      </tr>
%   #endfor
    </table>
% #endif

