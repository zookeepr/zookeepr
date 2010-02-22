<%inherit file="/base.mako" />

<h2>List of streams</h2>

% if len(c.stream_collection) > 0:
<table>
  <tr>
    <th>Name</th>
    <th>&nbsp;</th>
  </tr>
%   for stream in c.stream_collection:
  <tr class="${ h.cycle('even', 'odd')}">
    <td>${ h.link_to(stream.name, url=h.url_for(action='view', id=stream.id)) }</td>
%       if c.can_edit:
%           for action in ['edit', 'delete']:
  <td>${ h.link_to(action, url=h.url_for(action=action, id=stream.id)) }</td>
%           endfor
%       endif
</tr>
%   endfor
</table>
% endif

% if c.can_edit:
    <p>${ h.link_to('New Stream', url=h.url_for(action='new')) }</p>
% endif
 
