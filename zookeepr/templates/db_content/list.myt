<h2>List of DB pages</h2>

<table>
    <tr>
        <th>ID/Edit</th>
        <th>Title</th>
        <th>Type</th>
        <th>URL</th>
        <th>Created</th>
        <th>Last updated</th>
        <th>Delete</th>
    </tr>

% for d in c.db_content_collection:
    <tr class="<% h.cycle('even', 'odd')%>">
        <td><% h.link_to(str(d.id) + ' (edit)', url=h.url(controller='db_content', action='edit', id=d.id)) %></td>
%   if h.is_news(d.type_id):
        <td><% h.link_to(str(d.title) + ' (view)', url=h.url(controller='db_content', action='view', id=d.id)) %></td>
%   else:
        <td><% d.title %></td>
%   #endif
        <td><% d.type.name %></td>
%   if d.url != '':
        <td><% h.link_to(d.url, url='/' + d.url) %></td>
%   else:
        <td>N/A</td>
%   #endif
        <td><% d.creation_timestamp.strftime("%Y-%m-%d&nbsp;%H:%M") %></td>
        <td><% d.last_modification_timestamp.strftime("%Y-%m-%d&nbsp;%H:%M") %></td>
        <td><% h.link_to('X (delete)', url=h.url(controller='db_content', action='delete', id=d.id)) %></td>
    </tr>
% #endfor
</table>
<p><% h.link_to('Add another', url=h.url(controller='db_content', action='new')) %></p>

<%method title>
List of DB pages - <& PARENT:title &>
</%method>

<%init>
</%init>
