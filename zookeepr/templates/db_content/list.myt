<h2>List of DB pages</h2>

<table>
    <tr>
        <th>ID/Edit</th>
        <th>Title</th>
        <th>URL</th>
        <th>Delete</th>
    </tr>

% for d in c.db_content_collection:
    <tr class="<% h.cycle('even', 'odd')%>">
        <td><% h.link_to(str(d.id) + ' (edit)', url=h.url(controller='db_content', action='edit', id=d.id)) %></td>
        <td><% h.link_to(d.title + ' (view)', url='/' + d.url) %></td>
        <td><% d.url %></td>
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
