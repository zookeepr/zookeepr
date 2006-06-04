<h2>Create a myLCA account</h2>

<p>Someone write something cool about what this account gives you and
stuff like that.</p>

<% c.errors %>

<% h.form(h.url(action='new')) %>
<& form.myt &>
<% h.submit("Create") %>
<% h.end_form() %>
