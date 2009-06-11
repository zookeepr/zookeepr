<%inherit file="/base.mako" />

    ${ h.form(h.url_for()) }
    <h2>Create Manual Invoice</h2>
    <input type="hidden" value="${ c.item_count }" id="invoice.item_count" name="invoice.item_count" />

    <p>Person ID: ${ h.text('invoice.person') }</p>
    <p>Due Date: ${ h.text('invoice.due_date') } <span style="font-size: smaller;">(DD/MM/YYYY). Setting this in the future reserves products.</span></p>

    <p>Invoice Items:</p>
    <table id="products">
        <thead>
            <tr>
                <th>Product</th>
                <th>Quantity</th>
                <th>Cost/Item (cents)</th>
            </tr>
        </thead>

%for i in range(0,c.item_count+1):
        <tr>
            <td>
                <div>
                    <select name="invoice.items-${ i }.product" id="invoice.items-${ i }.product" onchange="return update_cost('${ i }');"><option value="0">--Select--</option>
%   for category in c.product_categories:
                        <optgroup label="${ category.name }">
%       for product in category.products:
                            <option value="${ product.id }">${ product.description }</option>
%       endfor
                        </optgroup>
%       endfor
                    </select>
                    <br />---> OR <input type="text" name="invoice.items-${ i }.description" size="55"/>
                </div>
            </td>
            <td><input type="text" name="invoice.items-${ i }.qty" id="invoice.items-${ i }.qty" size="3" onchange="return update_total();" value="1" /></td>
            <td><input type="text" name="invoice.items-${ i }.cost" id="invoice.items-${ i }.cost" size="6" onchange="return update_total();" value="0" /></td>
        </tr>
%endfor

        <tfoot>
            <tr>
                <td><a href="#" onclick="return add_product_item('products');">Add</a> / <a href="#" onclick="return remove_product_item('products');">Remove</a></td>
                <td style="text-align: right;"><a href="#" onclick="return update_total();" style="font-size: smaller;">(update)</a> Total: </td>
                <td>$<span id="total">0.00</span></td>
            </tr>
        </tfoot>
    </table>
    <p>${ h.submit('submit', 'Save') }</p>
    ${ h.end_form() }

<%def name="title()">
Create Invoice - ${ parent.title() }
</%def>

<%def name="extra_head()">
<script type="text/javascript">
function add_product_item(table)
{
    product_table = document.getElementById(table);
    last_row = product_table.rows.length;
    
    i = last_row - 2;
    row = product_table.insertRow(i+1);
   
    new_product = document.createElement('select');
    new_product.setAttribute('name', 'invoice.items-' + i + '.product'); new_product.setAttribute('id', 'invoice.items-' + i + '.product');
    new_product.setAttribute('onchange', 'return update_cost("' + i + '");');
        product = document.createElement('option');
        product.setAttribute('value', '0');
        product.appendChild(document.createTextNode("--Select--"));
    new_product.appendChild(product);
%for category in c.product_categories:
        cat = document.createElement('optgroup');
        cat.setAttribute('label', '${ category.name }');
%   for product in category.products:
            product = document.createElement('option');
            product.setAttribute('value', '${ product.id }');
            product.appendChild(document.createTextNode("${ product.description }"));
            cat.appendChild(product);
%   endfor
        new_product.appendChild(cat);
%endfor

    new_description = document.createElement('input');
    new_description.setAttribute('type', 'text');
    new_description.setAttribute('name', 'invoice.items-' + i + '.description');
    new_description.setAttribute('size', '55');

    new_qty = document.createElement('input');
    new_qty.setAttribute('type', 'text');
    new_qty.setAttribute('name', 'invoice.items-' + i + '.qty');    new_qty.setAttribute('id', 'invoice.items-' + i + '.qty');
    new_qty.setAttribute('size', '3');
    new_qty.setAttribute('onchange', 'return update_total();');
    new_qty.setAttribute('value', '1');

    new_cost = document.createElement('input');
    new_cost.setAttribute('type', 'text');
    new_cost.setAttribute('name', 'invoice.items-' + i + '.cost');  new_cost.setAttribute('id', 'invoice.items-' + i + '.cost');
    new_cost.setAttribute('size', '6');
    new_cost.setAttribute('onchange', 'return update_total();');
    new_cost.setAttribute('value', '0');
   
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

function update_cost(i)
{
    product_field = document.getElementById('invoice.items-' + i + '.product');
    cost = document.getElementById('invoice.items-' + i + '.cost');
    product_cost_array = new Array();
%for category in c.product_categories:
%   for product in category.products:
    product_cost_array[${ product.id }] = ${ product.cost };
%   endfor
%endfor

    cost.value = product_cost_array[product_field.value];
    return update_total();
}

function remove_product_item(table)
{
    product_table = document.getElementById(table);
    last_row = product_table.rows.length;

    i = last_row - 1;
    if (last_row > 3)
    {
        product_table.deleteRow(i - 1);
        document.getElementById('invoice.item_count').value = i - 3;
    }
    
    return update_total();
}

function update_total()
{
    total = document.getElementById("total");
    amount = 0;
    
    for (i = 0; i <= document.getElementById('invoice.item_count').value; i++ )
    {
        amount += parseInt(document.getElementById('invoice.items-' + i + '.cost').value) * parseInt(document.getElementById('invoice.items-' + i + '.qty').value);
    }

    total.innerHTML = amount;

    return false;
}
</script>
</%def>
