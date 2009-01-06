    <h2>View product</h2>

    <p><b>Description:</b> <% c.product.description | h %><br></p>
    <p><b>Category:</b> <% c.product.category.name %><br></p>
    <p><b>Active:</b> <% h.yesno(c.product.active) %><br></p>
    <p><b>Cost:</b> <% h.number_to_currency(c.product.cost/100.0) | h %><br></p>
    <p><b>Auth code:</b> <% c.product.auth | h %><br></p>
    <p><b>Validate code:</b> <% c.product.validate | h %><br></p>

    <h3>Product Totals</h3>
    <p><b>Note:</b> Totals are not necessarily accurate as they do not take into account for vouchers. They are simply paid items times cost.</p>
    <p><b>Invoiced (inc. overdue):</b> <% c.product.qty_invoiced(date = False) %></p>
    <p><b>Invoiced:</b> <% c.product.qty_invoiced() %></p>
    <p><b>Sold:</b> <% c.product.qty_sold() %></p>
    <p><b>Total:</b> <% h.number_to_currency((c.product.qty_sold() * c.product.cost)/100) %></p>

    <h3>Included Products</h3>
    <table>
      <thead><tr>
        <th>Name</th>
        <th>Qty</th>
      </tr></thead>
%for iproduct in c.product.included:
      <tr>
        <td><% iproduct.include_category.name %></td>
        <td><% iproduct.include_qty %></td>
      </tr>
%#endfor
    </table>

    <h3>This Products Ceilings</h3>
    <table>
      <thead><tr>
        <th>Name</th>
        <th>Limit</th>
        <th>Available From</th>
        <th>Available Until</th>
        <th>Available</th>
        <th>Invoiced</th>
        <th>Sold</th>
      </tr></thead>
%for ceiling in c.product.ceilings:
      <tr>
        <td><% h.link_to(ceiling.name, url=h.url(controller='ceiling', action='view', id=ceiling.id)) %></td>
        <td><% ceiling.max_sold %></td>
%    if ceiling.available_from:
        <td><% ceiling.available_from.strftime('%d/%m/%y') %></td>
%    else:
        <td></td>
%    #endif
%    if ceiling.available_until:
        <td><% ceiling.available_until.strftime('%d/%m/%y') %></td>
%    else:
        <td></td>
%    #endif
        <td><% h.yesno(ceiling.available()) %></td>
        <td><% ceiling.qty_invoiced() %></td>
        <td><% ceiling.qty_sold() %></td>
      </tr>
%#endfor
    </table>

    <h3>This Product Sales</h3>
    <table>
      <thead><tr>
        <th>Invoice</th>
        <th>Person</th>
        <th>Qty</th>
        <th>Status</th>
      </tr></thead>
%for invoice_item in c.product.invoice_items:
%    if invoice_item.invoice.paid():
      <tr>
        <td><% h.link_to('id: ' + str(invoice_item.invoice.id), url=h.url(controller='invoice', action='view', id=invoice_item.invoice.id)) %></td>
        <td><% h.link_to(invoice_item.invoice.person.firstname + ' ' + invoice_item.invoice.person.lastname, h.url(controller='person', action='view', id=invoice_item.invoice.person.id)) %></td>
        <td><% invoice_item.qty %></td>
        <td><% invoice_item.invoice.status() %></td>
      </tr>
%    #endif
%#endfor
    </table>

    <h3>This Product Invoices</h3>
    <table>
      <thead><tr>
        <th>Invoice</th>
        <th>Person</th>
        <th>Qty</th>
        <th>Status</th>
      </tr></thead>
%for invoice_item in c.product.invoice_items:
%    if not invoice_item.invoice.void and not invoice_item.invoice.paid():
      <tr>
        <td><% h.link_to('id: ' + str(invoice_item.invoice.id), url=h.url(controller='invoice', action='view', id=invoice_item.invoice.id)) %></td>
        <td><% h.link_to(invoice_item.invoice.person.firstname + ' ' + invoice_item.invoice.person.lastname, h.url(controller='person', action='view', id=invoice_item.invoice.person.id)) %></td>
        <td><% invoice_item.qty %></td>
        <td><% invoice_item.invoice.status() %></td>
      </tr>
%    #endif
%#endfor
    </table>

    <h3>Invalid Sales</h3>
    <table>
      <thead><tr>
        <th>Invoice</th>
        <th>Person</th>
        <th>Qty</th>
        <th>Status</th>
      </tr></thead>
%for invoice_item in c.product.invoice_items:
%    if not invoice_item.invoice.paid() and invoice_item.invoice.void:
      <tr>
        <td><% h.link_to('id: ' + str(invoice_item.invoice.id), url=h.url(controller='invoice', action='view', id=invoice_item.invoice.id)) %></td>
        <td><% h.link_to(invoice_item.invoice.person.firstname + ' ' + invoice_item.invoice.person.lastname, h.url(controller='person', action='view', id=invoice_item.invoice.person.id)) %></td>
        <td><% invoice_item.qty %></td>
        <td><% invoice_item.invoice.status() %></td>
      </tr>
%    #endif
%#endfor
    </table>

    <p>
% if c.can_edit:
      <% h.link_to('Edit', url=h.url(action='edit',id=c.product.id)) %> |
% #end if
      <% h.link_to('Back', url=h.url(action='index', id=None)) %>
    </p>
