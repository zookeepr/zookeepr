    <&| @zookeepr.lib.form:fill, defaults=defaults, errors=errors &>
    <% h.form(h.url()) %>
    <h2>Create Manual Invoice</h2>
    <input type="hidden" value="1" id="invoice.item_count" name="invoice.item_count" />

    <p>Person ID: <% h.textfield('invoice.person') %></p>
    <p>Due Date: <% h.textfield('invoice.due_date') %> <span style="font-size: smaller;">(DD/MM/YYYY). Setting this in the future reserves products.</span></p>

    <p>Invoice Items:</p>
    <table id="products">
        <thead>
            <tr>
                <th>Product</th>
                <th>Quantity</th>
                <th>Cost/Item (cents)</th>
            </tr>
        </thead>

%for i in range(0,c.item_count):
        <tr>
            <td>
                <div>
                    <select name="invoice.items-<% i %>.product"><option value="0">--Select--</option>
%   for category in c.product_categories:
                        <optgroup label="<% category.name %>">
%       for product in category.products:
                            <option value="<% product.id %>"><% product.description %></option>
%       #endfor
                        </optgroup>
%       #endfor
                    </select>
                    <br />---> OR <input type="text" name="invoice.items-<% i %>.description" size="55"/>
                </div>
            </td>
            <td><input type="text" name="invoice.items-<% i %>.qty" size="3"/></td>
            <td><input type="text" name="invoice.items-<% i %>.cost" size="6"/></td>
        </tr>
%#endfor

        <tfoot>
            <tr>
                <td><a href="#" onclick="return add_product_item('products');">Add</a> / <a href="#" onclick="return remove_product_item('products');">Remove</a></td>
                <td style="text-align: right;"><a href="#" onclick="return update_total('total');" style="font-size: smaller;">(update)</a> Total: </td>
                <td>$<span id="total">0.00</span></td>
            </tr>
        </tfoot>
    </table>
    <p><% h.submitbutton('Save') %></p>
    <% h.end_form() %>
    </&>
<%args>
defaults
errors
</%args>

<%init>
</%init>

<%method title>
Create Invoice - <& PARENT:title &>
</%method>

<%method extra_head>
<script type="text/javascript">
function add_product_item(table)
{
    product_table = document.getElementById(table);
    last_row = product_table.rows.length;
    
    i = last_row - 1;
    row = product_table.insertRow(i);
   
    new_product = document.createElement('select');
    new_product.setAttribute('name', 'invoice.items-' + i + '.product');
        product = document.createElement('option');
        product.setAttribute('value', '0');
        product.appendChild(document.createTextNode("--Select--"));
    new_product.appendChild(product);
%for category in c.product_categories:
        cat = document.createElement('optgroup');
        cat.setAttribute('label', '<% category.name %>');
%   for product in category.products:
            product = document.createElement('option');
            product.setAttribute('value', '<% product.id %>');
            product.appendChild(document.createTextNode("<% product.description %>"));
            cat.appendChild(product);
%   #endfor
        new_product.appendChild(cat);
%#endfor

    new_description = document.createElement('input');
    new_description.setAttribute('type', 'text');
    new_description.setAttribute('name', 'invoice.items-' + i + '.description');
    new_description.setAttribute('size', '55');

    new_qty = document.createElement('input');
    new_qty.setAttribute('type', 'text');
    new_qty.setAttribute('name', 'invoice.items-' + i + '.qty');
    new_qty.setAttribute('size', '3');
    
    new_cost = document.createElement('input');
    new_cost.setAttribute('type', 'text');
    new_cost.setAttribute('name', 'invoice.items-' + i + '.cost');
    new_cost.setAttribute('size', '6');
   
    new_item = document.createElement('div');
    new_item.appendChild(new_product);
    new_item.appendChild(document.createElement('br'));
    new_item.appendChild(document.createTextNode("---> OR "));
    new_item.appendChild(new_description);

    row.insertCell(0).appendChild(new_item);
    row.insertCell(1).appendChild(new_qty);
    row.insertCell(2).appendChild(new_cost);

    document.getElementById('invoice.item_count').value = i;

    return false;
}

function remove_product_item(table)
{
    product_table = document.getElementById(table);
    last_row = product_table.rows.length;

    i = last_row - 1;
    if (last_row > 2)
    {
        product_table.deleteRow(i - 1);
    }
    
    return false;
}

function update_total(total_span)
{
    total = document.getElementById(total_span);
    total.innerHTML = "coming soon...";
    
    return false;
}
</script>
</%method>
