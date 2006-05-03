<% h.form(h.url_for()) %>

<p>
<label for="username">Username:</label>
<br />
<% h.text_field('username') %>
</p>

<p>
<label for="age">Age:</label>
<br />
<% h.text_field('age') %>
</p>

<% h.submit('Send it') %>
<% h.end_form() %>
