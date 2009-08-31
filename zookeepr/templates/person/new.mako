<%inherit file="/base.mako" />
<%
    c.form = 'new'
%>
<h2 class="pop">New user account creation</h2>

<p>Enter your name, and email address, and password, and we'll email you with a confirmation to create your account.</p>

<p>
If you've already got an account but can't log in, you can
${ h.link_to('recover your password', url=h.url_for(action='forgotten_password')) }.
</p>

${ h.form(h.url_for(), method='post') }

<%include file="form.mako" />

<p class="submit">${ h.submit("submit", "Create a new account",) }</p>

${ h.end_form() }

