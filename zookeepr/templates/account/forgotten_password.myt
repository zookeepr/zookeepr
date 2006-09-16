<&| @zookeepr.lib.form:fill, defaults=defaults, errors=errors &>
<form method="post" action="<% h.url_for() %>" >
<fieldset>
<h3>Forgotten password?</h3>
<p>Enter your email address and an email will be sent to you allowing you to
   select a new password.
</p>
<div class="centre">
<% h.text_field('email_address', size=30) %>
<% h.submit("Set a new password") %>
</div>


</fieldset>

</form>
</&>

<%args>
defaults
errors
</%args>
