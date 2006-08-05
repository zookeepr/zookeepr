<h2>Delete submission <% c.submission.id %></h2>

<% h.form(h.url_for()) %>
<p> Are you sure you want to delete the submission entitled '<% c.submission.title %>'?</p>
<% h.hidden_field('delete', 'ok') %>
<% h.submit('Delete') %>
<% h.end_form() %>
# or <% h.link_to('No, take me back.', url=h.url(action='index', id=None)) %>
