<%inherit file="/base.mako" />
<p>
To complete the password reset process please follow the instructions sent to your email address,
<i>${ c.email }</i>.
</p>

<p>
If you do not receive this email within a reasonable timeframe, please contact us at ${ h.email_link_to(c.config.get('contact_email')) }.
</p>
