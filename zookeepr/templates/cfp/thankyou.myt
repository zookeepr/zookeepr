<h2>Call for Participation</h2>

<h3>Thank You</h3>

<p>
Thank you for your proposal. 
</p>

<p>
An email has been sent to you at <em><% c.registration.email_address | h %></em> with details of your proposal.  To complete the registration process (allowing you to log in again later and modify your proposal) please follow the instructions in that message.
</p>

<p>
If you wish to make a second proposal, or modify the one you have just made, please first complete the registration, and <% h.link_to('sign in', url=h.url(controller='account', action='signin', id=None)) %>.
</p>

<p>
If you do not receive this message in a reasonable timeframe, please contact us at <% h.ctte_email() %>
</p>

<p>
<a href="<% h.url_for("home") %>">Click here</a> to return to the main page.
</p>
