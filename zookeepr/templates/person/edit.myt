<h2>Edit person</h2>

<% h.form(h.url(id=c.person.id)) %>
<& form.myt &>
<% h.submit('Update') %>
<% h.end_form() %>
<% h.link_to('back', url=h.url(action='index', id=None)) %>
