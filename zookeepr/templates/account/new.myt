<&| @zookeepr.lib.form:fill, defaults=defaults, errors=errors &>
<form method="post" action="<% h.url_for() %>" >
<fieldset>
<h3>New user account creation</h3>
<p>Enter your name, and email address, and we'll email you with a confirmation to create your account.
<div class="centre">
<% h.text_field('registration.fullname', size=30) %>
<% h.text_field('registration.email_address', size=30) %>
<% h.text_field('registration.handle', size=30) %>
<% h.submit("Create a new account") %>
</div>


</fieldset>

</form>
</&>

<%args>
defaults
errors
</%args>
