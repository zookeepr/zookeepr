
# FIXME: dirty hack because this shouldn't exist
<h1>Delete cfp</h1>

<% h.form(h.url_for()) %>
<p> Are you sure you want to delete this cfp?</p>
<% h.submit('Delete') %>
<% h.end_form() %> or <% h.link_to('No, take me back.', url=h.url(action='index', id=None)) %>
