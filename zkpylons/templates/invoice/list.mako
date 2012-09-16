<%inherit file="/base.mako" />

% if c.can_edit:
    <p>${ h.link_to('Create new (manual) Invoice', h.url_for(action='new')) }</p>
% endif
    <p style="font-size: smaller;">Unvoiding invoices marks them as manual.</p>
    <table>
      <tr>
        <th>rego</th>
        <th>invoice</th>
        <th>created</th>
        <th>person</th>
        <th>amount</th>
        <th>status</th>
        <th>manual</th>
        <th>payment(s)</th>
      </tr>
% for i in c.invoice_collection:
      <tr class="${ h.cycle('even', 'odd')}">
%   if i.person.registration:
<%       r = i.person.registration %>
          <td>${ h.link_to('id: ' + str(r.id), h.url_for(controller='registration', action='view', id=r.id)) }</td>
%   else:
          <td>-</td>
%   endif
        <td>${ h.link_to('id: ' + str(i.id), h.url_for(action='view', id=i.id)) }</td>
        <td>${ i.creation_timestamp |h }</td>
        </td>
        <td>${ h.link_to(i.person.firstname + ' ' + i.person.lastname, h.url_for(controller='person', action='view', id=i.person.id)) }</td>
        <td align="right">${ h.integer_to_currency(i.total) }</td>
        <td>${ i.status }
%   if i.status == 'Unpaid' or i.total == 0:
            <span style="font-size: smaller;">(${ h.link_to('Void', h.url_for(action="void", id=i.id)) })</span>
%   endif
%   if i.status == 'Invalid':
            <span style="font-size: smaller;">(${ h.link_to('Unvoid', h.url_for(action="unvoid", id=i.id)) })</span>
%   endif
        </td>
        <td>${ h.yesno(i.manual) |n }</td>
        <td>
%   if len(i.good_payments) > 0:
%       for p in i.good_payments:
%           if p.amount_paid != i.total:
          <b>mismatch!</b>
%           endif
          ${ h.integer_to_currency(p.amount_paid) }
          <small>${ p.gateway_ref |h}</small>
%       endfor
%   elif len(i.bad_payments) > 0:
        Bad payment(s)!
%   else:
          -
%   endif
        </td>
        </td>
      </tr>
% endfor
    </table>
