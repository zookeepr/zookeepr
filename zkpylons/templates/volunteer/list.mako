<%inherit file="/base.mako" />

<h2>List of Volunteers</h2>
% if len(c.volunteer_collection) > 0:

    <table>
      <thead>
        <tr>
          <th>Volunteer</th>
          <th>Person</th>
          <th>Name</th>
          <th>E-Mail</th>
          <th>Phone Number</th>
          <th>Other</th>
          <th>Status</th>
          <th>Ticket Price</th>
          <th>&nbsp;</th>
%   if c.can_edit:
          <th>&nbsp;</th>
%   endif
        </tr>
      </thead>
%   for volunteer in c.volunteer_collection:
      <tr class="${ h.cycle("even", "odd") }">
        <td>${ h.link_to('id: ' + str(volunteer.id), url=h.url_for(action='view', id=volunteer.id)) }</td>
        <td>${ h.link_to('id: ' + str(volunteer.person.id), url=h.url_for(controller='person', action='view', id=volunteer.person.id)) }</td>
        <td>${ h.link_to(volunteer.person.firstname + ' ' + volunteer.person.lastname, h.url_for(controller='person', action='view', id=volunteer.person.id)) }</td>
        <td>${ volunteer.person.email_address }</td>
        <td>${ volunteer.person.mobile or volunteer.person.phone | h }</td>
        <td>${ h.line_break(volunteer.other) }</td>
%       if volunteer.accepted is None:
        <td>Pending</td>
%       elif volunteer.accepted == True:
        <td>Accepted</td>
%       else:
        <td>Rejected</td>
%       endif
%       if volunteer.ticket_type:
        <td>${ h.integer_to_currency(volunteer.ticket_type.cost) }</td>
%       else:
        <td>No Ticket</td>
%       endif
        <td>
%       if volunteer.accepted != True:
          ${ h.link_to('accept', url=h.url_for(action='accept', id=volunteer.id)) }
%       else:
          ${ h.link_to('change ticket', url=h.url_for(action='accept', id=volunteer.id)) }
%       endif
%       if volunteer.accepted is not None:
          ${ h.link_to('pending', url=h.url_for(action='pending', id=volunteer.id)) }
%       endif
%       if volunteer.accepted != False:
          ${ h.link_to('reject', url=h.url_for(action='reject', id=volunteer.id)) }
%       endif
        </td>
%       if c.can_edit:
        <td>${ h.link_to('edit', url=h.url_for(action='edit', id=volunteer.id)) }</td>
%       endif
      </tr>
%   endfor
    </table>
% endif

