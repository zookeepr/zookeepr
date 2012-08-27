<%inherit file="/base.mako" />

<h2>List Proposal Statuss</h2>

% if len(c.proposal_status_collection) > 0:
<table>
  <tr>
    <th>id</th>
    <th>Name</th>
    <th>&nbsp;</th>
    <th>&nbsp;</th>
  </tr>
%   for proposal_status in c.proposal_status_collection:
  <tr class="${ h.cycle('even', 'odd')}">
    <td>${ h.link_to(proposal_status.id, url=h.url_for(action='view', id=proposal_status.id)) }</td>
    <td>${ proposal_status.name }</td>
%       if c.can_edit:
%           for action in ['edit', 'delete']:
  <td>${ h.link_to(action, url=h.url_for(action=action, id=proposal_status.id)) }</td>
%           endfor
%       endif
</tr>
%   endfor
</table>
% endif

% if c.can_edit:
    <p>${ h.link_to('New Proposal Status', url=h.url_for(action='new')) }</p>
% endif
 
