<&| @zookeepr.lib.form:fill, defaults=defaults, errors=errors &>
<form method="post" action="<% h.url_for() %>" >
<fieldset>
<h3>Forgotten password?</h3>
<p>Enter your email address and an email will be sent to you allowing you to
   select a new password.
</p>
<div class="centre">
<p class="label"><span class="mandatory">*</span>Email address:</p>
<p class="entries"><% h.textfield('email_address', size=60) %></p>
<p class="submit"><% h.submitbutton("Set a new password") %></p>
</div>


</fieldset>

</form>
</&>

<%args>
defaults
errors
</%args>
