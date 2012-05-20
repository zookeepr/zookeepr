<%inherit file="/base.mako" />

<h2>List of Registration Notes</h2>

<table>
    <tr>
        <th>ID/Edit</th>
        <th>Event</th>
        <th>Vote tokens</th>
        <th>Comment</th>
        <th>Created</th>
        <th>Last updated</th>
        <th>Delete</th>
    </tr>

% for d in c.vote_collection:
<%   print d %>
    <tr class="${ h.cycle('even', 'odd')}">
        <td>${ h.link_to(str(d.id) + ' (edit)', url=h.url_for(controller='vote', action='edit', id=d.id)) }</td>
        <td>${ h.link_to(d.event.name, h.url_for(controller='event', action='view', id=d.event.id)) }</td>
        <td>${ d.vote_value }</td>
        <td>${ h.line_break(d.comment) }
        <td>${ d.creation_timestamp.strftime("%Y-%m-%d&nbsp;%H:%M") | n}</td>
        <td>${ d.last_modification_timestamp.strftime("%Y-%m-%d&nbsp;%H:%M") | n}</td>
        <td>${ h.link_to('X (delete)', url=h.url_for(controller='vote', action='delete', id=d.id)) }</td>
    </tr>
% endfor
</table>
<p>${ h.link_to('Add another', url=h.url_for(controller='vote', action='new')) }</p>

<%def name="title()">
List of DB pages - ${ parent.title() }
</%def>
