<%inherit file="/base.mako" />
<p>
A password recovery process is already in progress for this account.
</p>

<p>
If you have any further problems or have not received an email to this address within a reasonable timeframe, please contact us on ${ h.email_link_to(c.config.get('contact_email')) } and we can sort this out.
</p>
