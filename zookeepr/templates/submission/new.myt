<h1>New submission</h1>

<% h.form(h.url(action='new')) %>
<& form.myt &>
<% h.submit("New") %>
<% h.end_form() %>

<% h.link_to('Back', url=h.url(action='index')) %>
