<% h.form(h.url(), multipart=True) %>
<& form.myt &>
<% h.submit('Participate!') %>
<% h.end_form() %>


<%method title>
Call for Participation - <& PARENT:title &>
</%method>
