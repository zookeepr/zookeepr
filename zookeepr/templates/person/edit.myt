<h1>Edit person</h1>

<% h.form(h.url(id=c.person.handle)) %>
<& form.myt &>
<% h.submit('Update') %>
<% h.end_form() %>
<% h.link_to('back', url=h.url(action='index', id=None)) %>
