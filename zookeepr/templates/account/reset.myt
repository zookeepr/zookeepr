<h1>reset password</h1>

<&| @zookeepr.lib.form:fill, defaults=defaults, errors=errors &>

<% h.form(url=h.url()) %>

<fieldset>
<legend>
set password
</legend>

<p>
Enter thenew password for <em><% c.conf_rec.email_address %></em> in the form below.
</p>

#<p>
#Your password 

<p>
<label for="password">New password:</label>
<% h.password_field('password') %>
</p>
<p>
<label for="password_confirm">Re-enter password:</label>
<% h.password_field('password_confirm') %>
</p>

<% h.submit() %>

<% h.end_form() %>

</&>

<%args>
defaults
errors
</%args>
