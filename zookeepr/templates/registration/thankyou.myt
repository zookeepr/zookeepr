<h2>Registration</h2>

<h3>Thank You</h3>

<p>
Thank you for your registration! 
</p>

<p>
An email has been sent to you at <em><% c.person.email_address | h %></em> with details of your registration. 
% if 'signed_in_person_id' in session:
To complete the registration process (generate and pay your
invoice) please go to the <a href="/registration/status">registration
status page</a>.
% else:
To complete the registration process (allowing you to log in again to modify your details and pay your invoice) please follow the instructions in that message.
% #endif
</p>

</p>
<p>
If you do not receive this message in a reasonable timeframe, please contact us at <% h.contact_email() %>
</p>

<p>
Return to
% if 'signed_in_person_id' in session:
the <a href="/registration/status">registration status page</a> or
% #endif
the <a href="<% h.url_for("home") %>">main page</a>.
</p>
