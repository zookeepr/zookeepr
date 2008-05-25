<h2>Delete proposal <% c.proposal.id %></h2>

<% h.form(h.url_for()) %>
<p> Are you sure you want to delete the proposal entitled '<% c.proposal.title %>'?</p>
<% h.hidden_field('delete', 'ok') %>
<% h.submitbutton('Delete') %>
<% h.end_form() %>
# or <% h.link_to('No, take me back.', url=h.url(action='index', id=None)) %>
