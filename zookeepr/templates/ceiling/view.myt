    <h2>View ceiling</h2>

    <p><b>Name:</b> <% c.ceiling.name %><br></p>
    <p><b>Limit:</b> <% c.ceiling.max_sold | h %><br></p>
    <p>
      <b>Available From:</b>
% if c.ceiling.available_from:
      <% c.ceiling.available_from.strftime('%d/%m/%y') | h %>
% #endif
      <br>
    </p>
    <p>
      <b>Available Until:</b>
% if c.ceiling.available_until:
      <% c.ceiling.available_until.strftime('%d/%m/%y') | h %>
% #endif
      <br>
    </p>
    <p><b>Currently Available:</b> <% h.yesno(c.ceiling.available()) %> <br></p>
    <p><b>Invoiced:</b> <% c.ceiling.qty_invoiced() | h %><br></p>
    <p><b>Sold:</b> <% c.ceiling.qty_sold() | h %><br></p>
% if len(c.ceiling.products) > 0:
    <h3>Products in this Ceiling</h3>
    <table>
      <tr>
        <th>Description</th>
        <th>Category</th>
        <th>Active</th>
        <th>Cost</th>
        <th>Invoiced</th>
        <th>Sold</th>
      </tr>
% for product in c.ceiling.products:
      <tr>
        <td><% h.link_to(product.description, url=h.url(controller='product', action='view', id=product.id)) %></td>
        <td><% product.category.name | h %></td>
        <td><% h.yesno(product.active) %></td>
        <td><% h.number_to_currency(product.cost/100.0) %></td>
        <td><% product.qty_invoiced() | h %></td>
        <td><% product.qty_sold() | h %></td>
      </tr>
% #endfor
    </table>
    <p>
% if c.can_edit:
    <% h.link_to('Edit', url=h.url(action='edit',id=c.ceiling.id)) %> |
% #end if
    <% h.link_to('Back', url=h.url(action='index', id=None)) %></p>
