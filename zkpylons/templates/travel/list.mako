<%inherit file="/base.mako" />

<h2>List Travels</h2>

% if len(c.travel_collection) > 0:
<table>
  <tr>
    <th>id</th>
    <th>Name</th>
    <th>Origin</th>
    <th>Destination</th>
    <th>&nbsp;</th>
    <th>&nbsp;</th>
  </tr>
%   for travel in c.travel_collection:
  <tr class="${ h.cycle('even', 'odd')}">
    <td>${ h.link_to(travel.id, url=h.url_for(action='view', id=travel.id)) }</td>
    <td>${ h.link_to(travel.person.fullname, h.url_for(controller='person', action='view', id=travel.person.id)) }</td>
    <td>${ travel.origin_airport }</td>
    <td>${ travel.destination_airport }</td>
%       if c.can_edit:
%           for action in ['edit', 'delete']:
    <td>${ h.link_to(action, url=h.url_for(action=action, id=travel.id)) }</td>
%           endfor
%       endif
  </tr>
%   endfor
</table>
% endif

% if c.can_edit:
    <p>${ h.link_to('New Travel', url=h.url_for(action='new')) }</p>
% endif
 
