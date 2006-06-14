<h2>Edit submission</h2>

<% h.form(h.url(id=c.submission.id)) %>
<& form.myt &>
<% h.submit('Update') %>
<% h.end_form() %>
<% h.link_to('back', url=h.url(action='index', id=None)) %>
