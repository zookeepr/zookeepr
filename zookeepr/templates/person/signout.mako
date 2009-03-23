<%inherit file="/base.mako" />
<h2 class="pop">Would you like to sign out?</h2>
<p>Please confirm you would like to sign out.</p>

${ h.form(h.url_for(controller='person', action='signout')) }

    <p class="submit">${ h.submit('Sign out', 'Sign out') }</p>

<% h.end_form() %>

