<h1>New role</h1>

<% h.form(h.url(action='new')) %>
<& form.myt &>
<% h.submitbutton("New") %>
<% h.end_form() %>

<% h.link_to('Back', url=h.url(action='index')) %>
