<%inherit file="/base.mako" />

<h2>List of special offers</h2>

% if len(c.special_offer_collection) > 0:
<table>
  <tr>
    <th>Enabled</th>
    <th>Name</th>
    <th>Description</th>
    <th>ID Name</th>
    <th>&nbsp;</th>
  </tr>
%   for offer in c.special_offer_collection:
  <tr class="${ h.cycle('even', 'odd')}">
    <td>${ h.yesno(offer.enabled) |n }</td>
    <td>${ h.link_to(offer.name, url=h.url_for(action='view', id=offer.id)) }</td>
    <td>${ offer.description | n}</td>
    <td>${ offer.id_name }</td>
%       if c.can_edit:
%           for action in ['edit', 'delete']:
  <td>${ h.link_to(action, url=h.url_for(action=action, id=offer.id)) }</td>
%           endfor
%       endif
</tr>
%   endfor
</table>
% endif

% if c.can_edit:
    <p>${ h.link_to('New Special Offer', url=h.url_for(action='new')) }</p>
% endif
 
