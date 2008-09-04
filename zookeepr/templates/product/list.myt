<h2>List products</h2>

% if len(c.product_categories) > 0:
%   for pc in c.product_categories:
<h3><% pc.name %></h3>
<table>
  <tr>
    <th>Active</th>
    <th>Description</th>
    <th>Cost</th>
  </tr>
%       if len(pc.products) > 0:
%           for st in c.product_collection:
<tr>
  <td><% st.active %></td>
  <td><% h.link_to(st.description, url=h.url(action='view', id=st.id)) %></td>
  <td><% st.cost %></td>
%               if c.can_edit:
%                   for action in ['edit', 'delete']:
  <td><% h.link_to(action, url=h.url(action=action, id=st.id)) %></td>
%                   #endfor
%               #endif
</tr>
%           #endfor
%       #endif
</table>
%   #endfor
% #endif


<%python>
#if c.prduct_pages.current.previous:
#    m.write(h.link_to('Previous page', url=h.url(page=c.product_pages.current.previous)) + '  ')
#if c.product_pages.current.next:
#    m.write(h.link_to('Next page', url=h.url(page=c.product_pages.current.next)))

m.write('<br>')
if c.can_edit:
    m.write(h.link_to('New product', url=h.url(action='new')))
</%python>
 
