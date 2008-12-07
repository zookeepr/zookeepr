    <h2>List products</h2>
% if len(c.product_categories) > 0:
    <table>
%   grand_total = 0
%   for category in c.product_categories:
      <tr>
        <td colspan="10" align="center"><h3><% category.name %></h3></td>
      </tr>
      <thead><tr>
        <th>Description</th>
        <th>Active</th>
        <th>Available</th>
        <th>Cost</th>
        <th>Invoiced (inc. overdue)</th>
        <th>Valid Invoices</th>
        <th>Sold</th>
        <th>Total</th>
        <th>&nbsp;</th>
        <th>&nbsp;</th>
      </tr></thead>
%       if len(category.products) > 0:
%           cat_total = 0
%           for product in category.products:
%               cat_total += (product.qty_sold() * product.cost)
      <tr>
        <td><% h.link_to(product.description, url=h.url(action='view', id=product.id)) %></td>
        <td><% h.yesno(product.active) %></td>
        <td><% h.yesno(product.available()) %></td>
        <td><% h.number_to_currency(product.cost/100.0) | h %></td>
        <td><% product.qty_invoiced(date = False) %></td>
        <td><% product.qty_invoiced() %></td>
        <td><% product.qty_sold() %></td>
        <td><% h.number_to_currency((product.qty_sold() * product.cost)/100) %></td>
%               if c.can_edit:
%                   for action in ['edit', 'delete']:
        <td><% h.link_to(action, url=h.url(action=action, id=product.id)) %></td>
%                   #endfor
%               #endif
      </tr>
%           #endfor
%           grand_total += cat_total
        <tr>
            <td colspan="7" style="font-weight: bold; text-align: right;">Sub-Total:</td>
            <td colspan="3"><% h.number_to_currency(cat_total/100) %></td>
        </tr>
%       #endif
%   #endfor
        <tr>
            <td colspan="7" style="font-weight: bold; text-align: right;">Grand Total:</td>
            <td colspan="3"><% h.number_to_currency(grand_total/100) %></td>
        </tr>
    </table>
% #endif


<%python>
#if c.product_pages.current.previous:
#    m.write(h.link_to('Previous page', url=h.url(page=c.product_pages.current.previous)) + '  ')
#if c.product_pages.current.next:
#    m.write(h.link_to('Next page', url=h.url(page=c.product_pages.current.next)))

if c.can_edit:
    m.write('    <p>' + h.link_to('New product', url=h.url(action='new')) + '</p>')
</%python>
 
