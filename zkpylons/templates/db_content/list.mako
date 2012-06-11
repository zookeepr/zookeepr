<%inherit file="/base.mako" />
<h2>List of DB pages</h2>

<table>
    <tr>
        <th>ID/Edit</th>
        <th>Title</th>
        <th>Type</th>
        <th>URL</th>
        <th>Created On</th>
        <th>Published</th>
        <th>Last updated</th>
        <th>Delete</th>
    </tr>

% for d in c.db_content_collection:
    <tr class="${ h.cycle('even', 'odd')}">
        <td>${ h.link_to(str(d.id) + ' (edit)', url=h.url_for(controller='db_content', action='edit', id=d.id)) }</td>
%   if d.is_news() or d.is_page():
        <td>${ h.link_to(str(d.title) + ' (view)', url=h.url_for(controller='db_content', action='view', id=d.id)) }</td>
%   else:
        <td>${ d.title }</td>
%   endif
        <td>${ d.type.name }</td>
%   if '://' in d.url:
        <td>${ h.link_to(d.url, url=d.url) }</td>
%   elif d.url != '':
        <td>${ h.link_to(d.url, url=('/' + d.url)) }</td>
%   else:
        <td>N/A</td>
%   endif
        <td>${ d.creation_timestamp.strftime("%Y-%m-%d %H:%M") }</td>
        <td>${ h.yesno(d.publish_timestamp <= h.datetime.now()) |n } ${ d.publish_timestamp.strftime("%Y-%m-%d %H:%M") }</td>
        <td>${ d.last_modification_timestamp.strftime("%Y-%m-%d %H:%M") }</td>
        <td>${ h.link_to('X (delete)', url=h.url_for(controller='db_content', action='delete', id=d.id)) }</td>
    </tr>
% endfor
</table>
<p>${ h.link_to('Add another', url=h.url_for(controller='db_content', action='new')) }</p>

<%def name="title()">
List of DB pages -
 ${ parent.title() }
</%def>
