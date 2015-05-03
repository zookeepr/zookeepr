<%inherit file="/base.mako" />

<p>
We've sent activation instructions to ${ c.person.email_address }. Please 
check your email and click the link provided to activate your account.</p>

<p>Once you've activated your account, <a href="javascript:window.location.reload()">refresh to continue</a>.</p>
