    <h2>List of Volunteers</h2>
% if len(c.volunteer_collection) > 0:

    <table>
      <thead>
        <tr>
          <th>Volunteer</th>
          <th>Registration</th>
          <th>Name</th>
          <th>E-Mail</th>
          <th>Phone Number</th>
          <th>Status</th>
          <th>&nbsp;</th>
          <th>&nbsp;</th>
          <th>Other</th>
        </tr>
      </thead>
%   for volunteer in c.volunteer_collection:
      <tr>
        <td><% h.link_to('id: ' + str(volunteer.id), url=h.url(action='view', id=volunteer.id)) %></td>
%       if volunteer.person.registration:
        <td><% h.link_to('id: ' + str(volunteer.person.registration.id), url=h.url(controller='registration', action='view', id=volunteer.person.registration.id)) %></td>
%       else:
        <td>&nbsp;</td>
%       #endif
        <td><% h.link_to(m.apply_escapes(volunteer.person.firstname + ' ' + volunteer.person.lastname, 'h'), h.url(controller='person', action='view', id=volunteer.person.id)) %></td>
        <td><% volunteer.person.email_address %></td>
        <td><% volunteer.person.mobile or volunteer.person.phone | h %></td>
%       if volunteer.accepted is None:
        <td>Pending</td>
%       elif volunteer.accepted == True:
        <td>Accepted</td>
%       else:
        <td>Rejected</td>
%       #endif
        <td>
%       if volunteer.accepted is None or not volunteer.accepted:
          <% h.link_to('accept', url=h.url(action='accept', id=volunteer.id)) %>
%       #endif
%       if volunteer.accepted is None or volunteer.accepted:
          <% h.link_to('reject', url=h.url(action='reject', id=volunteer.id)) %>
%       #endif
        </td>
%       if c.can_edit:
        <td><% h.link_to('edit', url=h.url(action='edit', id=volunteer.id)) %></td>
%       #endif
        <td><% volunteer.other %></td>
      </tr>
%   #endfor
    </table>
% #endif

