    <h2>View ceiling</h2>

    <p><b>Name:</b> <% c.ceiling.name %><br></p>
    <p><b>Ceiling Limit:</b> <% c.ceiling.max_sold | h %><br></p>
    <p><b>Available From:</b> <% c.ceiling.available_from | h %><br></p>
    <p><b>Available Until:</b> <% c.ceiling.available_until | h %><br></p>
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
        <td><% product.description | h %></td>
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
