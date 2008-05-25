<h1>Edit role</h1>

<% h.form(h.url(id=c.role.id)) %>
<& form.myt &>
<% h.submitbutton('Update') %>
<% h.end_form() %>
<% h.link_to('back', url=h.url(action='index', id=None)) %>
