<%inherit file="/base.mako" />

<h2>Payment Gateway Error</h2>

<p>There was an internal error while talking to the payment gateway:
<blockquote><tt>${c.error_msg}</tt></blockquote></p>

<p>Please let us know at <a href="mailto:${ h.lca_info['webmaster_email'] }">${ h.lca_info['webmaster_email'] }</a></p>

