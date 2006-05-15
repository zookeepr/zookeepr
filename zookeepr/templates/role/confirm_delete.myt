<h1>Delete role</h1>

<% h.form(h.url_for()) %>
<p> Are you sure you want to delete this object?</p>
<% h.hidden_field('delete', 'ok') %>
<% h.submit('Delete') %>
<% h.end_form() %> or <% h.link_to('No, take me back.', url=h.url(action='index', id=None)) %>
