<h2>View product</h2>

<p><b>Description:</b> <% c.product.description | h %><br></p>
<p><b>Category:</b> <% c.product.category.name %><br></p>
<p><b>Active:</b> <% c.product.active | h %><br></p>
<p><b>Cost:</b> <% h.number_to_currency(c.product.cost/100.0) | h %><br></p>
<p><b>Auth code:</b> <% c.product.auth | h %><br></p>
<p><b>Validate code:</b> <% c.product.validate | h %><br></p>


<p>
% if c.can_edit:
<% h.link_to('Edit', url=h.url(action='edit',id=c.product.id)) %> |
% #end if
<% h.link_to('Back', url=h.url(action='index', id=None)) %></p>
