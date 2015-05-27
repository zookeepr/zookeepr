<%inherit file="/base.mako" />

<h2>List of Registration Notes</h2>

<table class="table sortable">
    <tr>
        <th>ID/Edit</th>
        <th>For person</th>
        <th>Note</th>
        <th>Block</th>
        <th>Written By</th>
        <th>Created</th>
        <th>Last updated</th>
        <th>Delete</th>
    </tr>

% for d in c.rego_note_collection:
<%   print d %>
    <tr class="${ h.cycle('even', 'odd')}">
        <td>${ h.link_to(str(d.id) + ' (edit)', url=h.url_for(controller='rego_note', action='edit', id=d.id)) }</td>
        <td>${ h.link_to(d.rego.person.firstname + ' ' + d.rego.person.lastname, h.url_for(controller='person', action='view', id=d.rego.person.id)) }, ${ h.link_to('View Registration', h.url_for(controller='registration', action='view', id=d.rego.id)) }</td>
        <td>${ h.line_break(d.note) }</td>
        <td>${ h.yesno(d.block) |n }</td>
        <td>${ h.link_to(d.by.firstname + ' ' + d.by.lastname, h.url_for(controller='person', action='view', id=d.by.id)) }</td>
        <td>${ d.creation_timestamp.strftime("%Y-%m-%d&nbsp;%H:%M") | n}</td>
        <td>${ d.last_modification_timestamp.strftime("%Y-%m-%d&nbsp;%H:%M") | n}</td>
        <td>${ h.link_to('X (delete)', url=h.url_for(controller='rego_note', action='delete', id=d.id)) }</td>
    </tr>
% endfor
</table>
<p>${ h.link_to('Add another', url=h.url_for(controller='rego_note', action='new')) }</p>

<%def name="title()">
List of DB pages - ${ parent.title() }
</%def>
