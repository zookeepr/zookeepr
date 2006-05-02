<h1>Edit submission</h1>

<% h.form(h.url(id=c.submission.id)) %>
<& form.myt &>
<% h.submit('Update') %>
<% h.end_form() %>
<% h.link_to('back', url=h.url(action='index', id=None)) %>
