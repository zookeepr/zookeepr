<%inherit file="/base.mako" />

<h2>List Event Types</h2>

% if len(c.event_type_collection) > 0:
<table class="table table-striped table-hover">
  <thead>
    <tr>
    <th>id</th>
    <th>Name</th>
    <th>&nbsp;</th>
    <th>&nbsp;</th>
    </tr>
  </thead>
%   for event_type in c.event_type_collection:
  <tr>
    <td>${ event_type.id }</td>
    <td>${ event_type.name }</td>
%       if c.can_edit:
%           for action in ['edit', 'delete']:
  <td>${ h.link_to(action, url=h.url_for(action=action, id=event_type.id)) }</td>
%           endfor
%       endif
</tr>
%   endfor
</table>
% endif

% if c.can_edit:
    <p>${ h.link_to('New Event Type', url=h.url_for(action='new')) }</p>
% endif
 
