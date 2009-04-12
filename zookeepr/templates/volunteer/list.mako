<%inherit file="/base.mako" />

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
        <td>${ h.link_to('id: ' + str(volunteer.id), url=h.url_for(action='view', id=volunteer.id)) }</td>
        <td>${ h.link_to('id: ' + str(volunteer.person.id), url=h.url_for(controller='person', action='view', id=volunteer.person.id)) }</td>
        <td>${ h.link_to(volunteer.person.firstname + ' ' + volunteer.person.lastname, h.url_for(controller='person', action='view', id=volunteer.person.id)) }</td>
        <td>${ volunteer.person.email_address }</td>
        <td>${ volunteer.person.mobile or volunteer.person.phone | h }</td>
%       if volunteer.accepted is None:
        <td>Pending</td>
%       elif volunteer.accepted == True:
        <td>Accepted</td>
%       else:
        <td>Rejected</td>
%       endif
        <td>
%       if volunteer.accepted is None or not volunteer.accepted:
          ${ h.link_to('accept', url=h.url_for(action='accept', id=volunteer.id)) }
%       endif
%       if volunteer.accepted is None or volunteer.accepted:
          ${ h.link_to('reject', url=h.url_for(action='reject', id=volunteer.id)) }
%       endif
        </td>
%       if c.can_edit:
        <td>${ h.link_to('edit', url=h.url_for(action='edit', id=volunteer.id)) }</td>
%       endif
        <td>${ h.line_break(volunteer.other) }</td>
      </tr>
%   endfor
    </table>
% endif

