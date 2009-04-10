<h2>People</h2>
<table>

% if len(c.person_collection) > 0:
  <tr>
    <th>id</th>
    <th>Email</th>
    <th>First Name</th>
    <th>Last Name</th>
    <th>Phone</th>
    <th>Mobile</th>
    <th>Created</th>
    <th>&nbsp;</th>
    <th>&nbsp;</th>
    <th>&nbsp;</th>
  </tr>
% #endif

% for p in c.person_collection:
  <tr>
    <td><% h.link_to(p.id, url=h.url(action='view', id=p.id)) %></td>
    <td><a href="mailto:<% p.email_address |h %>"><% p.email_address |h %></a></td>
    <td><% p.firstname |h %></td>
    <td><% p.lastname |h %></td>
    <td><% p.phone |h %></td>
    <td><% p.mobile |h %></td>
    <td><% p.creation_timestamp |h %></td>

%   for action in ['roles', 'view', 'edit']:
    <td><% h.link_to(action, url=h.url(action=action, id=p.id)) %></td>
%   #endfor
  </tr>
% #endfor
</table>


<%python>
#if c.person_pages.current.previous:
#    m.write(h.link_to('Previous page', url=h.url(page=c.person_pages.current.previous)) + '  ')
#if c.person_pages.current.next:
#    m.write(h.link_to('Next page', url=h.url(page=c.person_pages.current.next)))

</%python>
