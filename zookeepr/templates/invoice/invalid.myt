<h2>Invoice invalid</h2>

<p>The invoice is marked invalid, probably because your chosen
accommodation option is now full or registration is now closed. Please
<a href="/registration/<% c.signed_in_person.registration.id %>/pay"
>regenerate your invoice</a> for more details, go to the <a
href="/registration/status">registration status page</a> or
<% h.contact_email('contact the committee') %> to clear up the
situation.</p>

