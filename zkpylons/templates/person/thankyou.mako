<%inherit file="/base.mako" />
<h2 class="pop">New Account</h2>

<h2>Thank You</h2>

<p>
An email has been sent to you at <em>${ c.person.email_address | h }</em> with details on how to complete the account registration process.
Please follow the instructions in that message.
</p>

<p>
If you do not receive this message in a reasonable timeframe, please contact us at ${ h.email_link_to(c.config.get('contact_email')) }
</p>

<p>
<a href="${ h.url_for("home") }">Click here</a> to return to the main page.
</p>
