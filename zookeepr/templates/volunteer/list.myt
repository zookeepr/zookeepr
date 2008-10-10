    <h2>List of Volunteers</h2>
% if len(c.volunteer_collection) > 0:

    <table>
      <tr>
        <th>Volunteer</th>
        <th>Registration</th>
        <th>Name</th>
        <th>Phone Number</th>
        <th>Status</th>
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
      </tr>
%   #endfor
    </table>
% #endif


<%python>
#if c.volunteer_pages.current.previous:
#    m.write(h.link_to('Previous page', url=h.url(page=c.volunteer_pages.current.previous)) + '  ')
#if c.volunteer_pages.current.next:
#    m.write(h.link_to('Next page', url=h.url(page=c.volunteer_pages.current.next)))

if c.can_edit:
    m.write('    <p>' + h.link_to('New volunteer', url=h.url(action='new')) + '</p>')
</%python>
 
