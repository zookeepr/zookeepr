<%inherit file="/base.mako" />

<h2>List ceilings</h2>

% if len(c.ceiling_collection) > 0:
<table>
  <tr>
    <th>Name</th>
    <th>Limit</th>
    <th>Available From</th>
    <th>Available Until</th>
    <th>Available</th>
    <th>Invoiced (inc. overdue)</th>
    <th>Valid Invoices</th>
    <th>Sold</th>
    <th>&nbsp;</th>
    <th>&nbsp;</th>
  </tr>
%   for ceiling in c.ceiling_collection:
  <tr>
    <td>${ h.link_to(ceiling.name, url=h.url_for(action='view', id=ceiling.id)) }</td>
    <td>${ ceiling.max_sold }</td>
%       if ceiling.available_from:
    <td>${ ceiling.available_from.strftime('%d/%m/%y') }</td>
%       else:
    <td></td>
%       endif
%       if ceiling.available_until:
    <td>${ ceiling.available_until.strftime('%d/%m/%y') }</td>
%       else:
    <td></td>
%       endif
    <td>${ h.yesno(ceiling.available()) | n }</td>
    <td>${ ceiling.qty_invoiced(date=False) }</td>
    <td>${ ceiling.qty_invoiced() }</td>
    <td>${ ceiling.qty_sold() }</td>
%       if c.can_edit:
%           for action in ['edit', 'delete']:
  <td>${ h.link_to(action, url=h.url_for(action=action, id=ceiling.id)) }</td>
%           endfor
%       endif
</tr>
%   endfor
</table>
% endif

% if c.can_edit:
    <p>${ h.link_to('New Ceiling', url=h.url_for(action='new')) }</p>
% endif
 
