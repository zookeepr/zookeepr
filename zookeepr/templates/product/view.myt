    <h2>View product</h2>

    <p><b>Description:</b> <% c.product.description | h %><br></p>
    <p><b>Category:</b> <% c.product.category.name %><br></p>
    <p><b>Active:</b> <% h.yesno(c.product.active) %><br></p>
    <p><b>Cost:</b> <% h.number_to_currency(c.product.cost/100.0) | h %><br></p>
    <p><b>Auth code:</b> <% c.product.auth | h %><br></p>
    <p><b>Validate code:</b> <% c.product.validate | h %><br></p>

% if len(c.product.included) > 0:
    <h3>Included Products</h3>
    <table>
      <tr>
        <th>Name</th>
        <th>Qty</th>
      </tr>
%   for iproduct in c.product.included:
      <tr>
        <td><% iproduct.include_category.name %></td>
        <td><% iproduct.include_qty %></td>
      </tr>
%   #endfor
    </table>
% #endif
% if len(c.product.ceilings) > 0:
    <h3>This Products Ceilings</h3>
    <table>
      <tr>
        <th>Name</th>
        <th>Limit</th>
        <th>Available From</th>
        <th>Available Until</th>
        <th>Available</th>
        <th>Invoiced</th>
        <th>Sold</th>
      </tr>
%   for ceiling in c.product.ceilings:
      <tr>
        <td><% h.link_to(ceiling.name, url=h.url(controller='ceiling', action='view', id=ceiling.id)) %></td>
        <td><% ceiling.max_sold %></td>
%       if ceiling.available_from:
        <td><% ceiling.available_from.strftime('%d/%m/%y') %></td>
%       else:
        <td></td>
%       #endif
%       if ceiling.available_until:
        <td><% ceiling.available_until.strftime('%d/%m/%y') %></td>
%       else:
        <td></td>
%       #endif
        <td><% h.yesno(ceiling.available()) %></td>
        <td><% ceiling.qty_invoiced() %></td>
        <td><% ceiling.qty_sold() %></td>
      </tr>
%   #endfor
    </table>
% #endif
    <p>
% if c.can_edit:
      <% h.link_to('Edit', url=h.url(action='edit',id=c.product.id)) %> |
% #end if
      <% h.link_to('Back', url=h.url(action='index', id=None)) %>
    </p>
