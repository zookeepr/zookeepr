<%inherit file="/base.mako" />

<h2>Payment Gateway Error</h2>

<p>There was an internal error while talking to the payment gateway:
<blockquote><tt>${c.error_msg}</tt></blockquote></p>

<p>Please let us know at ${ h.email_link_to(c.config.get('webmaster_email')) }</p>

