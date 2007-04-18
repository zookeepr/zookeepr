<h2>New Account</h2>

<h3>Thank You</h3>

<p>
An email has been sent to you at <em><% c.person.email_address | h %></em> with details on how to complete the account registration process.
Please follow the instructions in that message.
</p>

<p>
If you do not receive this message in a reasonable timeframe, please contact us at <% h.contact_email() %>.
</p>

<p>
<a href="<% h.url_for("home") %>">Click here</a> to return to the main page.
</p>
