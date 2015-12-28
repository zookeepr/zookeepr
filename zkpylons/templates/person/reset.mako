<%inherit file="/base.mako" />
<h2>Reset Password</h2>

${ h.form(url=h.url_for(), id='reset-form') }

<p>
Enter the new password for <em>${ c.conf_rec.email_address }</em> in the form below.
</p>

<p class="label"><label for="password">New password:</label>
<p class="entries">${ h.password('password') }</p>

<p class="label"><label for="password_confirm">Re-enter password:</label></p>
<p class="entries">${ h.password('password_confirm') }</p>
</p>

<p class="submit">${ h.submit('reset', "Reset Password") }</p>

${ h.end_form() }
