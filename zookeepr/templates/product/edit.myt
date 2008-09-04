<h2>Edit product</h2>

<&| @zookeepr.lib.form:fill, defaults=defaults, errors=errors &>

<% h.form(h.url(id=c.product.id)) %>
<& form.myt &>
<p><% h.submitbutton('Update') %> <% h.link_to('back', url=h.url(action='index', id=None)) %></p>
<% h.end_form() %>

</&>

<%args>
defaults
errors
</%args>

<%init>
if not defaults and c.product:
    defaults = {
        'product.category': c.product.category.id,
        'product.description': c.product.description,
        'product.cost': c.product.cost,
    }
    if c.product.active:
        defaults['product.active'] = 1
    else:
        defaults['product.active'] = 0

</%init>
