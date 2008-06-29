<h2>reset password</h2>

<&| @zookeepr.lib.form:fill, defaults=defaults, errors=errors &>

<% h.form(url=h.url()) %>

<fieldset>
<legend>
set password
</legend>

<p>
Enter the new password for <em><% c.conf_rec.email_address %></em> in the form below.
</p>

#<p>
#Your password 

<p class="label"><label for="password">New password:</label>
<p class="entries"><% h.password_field('password') %></p>

<p class="label"><label for="password_confirm">Re-enter password:</label></p>
<p class="entries"><% h.password_field('password_confirm') %></p>
</p>

<p class="submit"><% h.submitbutton("Reset Password") %></p>

<% h.end_form() %>

</&>

<%args>
defaults
errors
</%args>
