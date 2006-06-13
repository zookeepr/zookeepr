<h1>Edit cfp</h1>

# FIXME: this page shouldn't exist, it's a hack to make the generics tests pass

<% h.form(h.url(id=c.cfp.id)) %>
<& form.myt &>
<% h.submit('Update') %>
<% h.end_form() %>
<% h.link_to('back', url=h.url(action='index', id=None)) %>
