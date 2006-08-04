<h2>Edit submission <% c.submission.id %></h2>

<div id="submission">

<% h.form(h.url()) %>
<& form.myt &>
<% h.submit('Update') %>
<% h.end_form() %>

</div>
