<h2>Sign up!</h2>

<p>
You must sign up to register or submit an event proposal.
</p>

<% c.errors %>

<% h.form(h.url(action='new')) %>
<& form.myt &>
<% h.submit("Create") %>
<% h.end_form() %>

<%method title>
Sign up! - <& PARENT:title &>
</%method>
