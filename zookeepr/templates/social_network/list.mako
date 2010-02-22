<%inherit file="/base.mako" />

<h2>List of Social Networks</h2>

% if len(c.social_networks) > 0:
<table>
  <tr>
    <th>Name</th>
    <th>Image</th>
    <th>URL</th>
    <th>&nbsp;</th>
  </tr>
%   for sn in c.social_networks:
  <tr class="${ h.cycle('even', 'odd')}">
    <td>${ h.link_to(sn.name, url=h.url_for(action='view', id=sn.id)) }</td>
    <td><img src="/images/${ sn.logo }" alt="${ sn.name } logo"></td>
    <td>${ sn.url }</td>
%       if c.can_edit:
%           for action in ['edit', 'delete']:
  <td>${ h.link_to(action, url=h.url_for(action=action, id=sn.id)) }</td>
%           endfor
%       endif
</tr>
%   endfor
</table>
% endif

% if c.can_edit:
    <p>${ h.link_to('New Social Network', url=h.url_for(action='new')) }</p>
% endif
 
<%def name="title()">
Social Network -
List All -
 ${ parent.title() }
</%def>
