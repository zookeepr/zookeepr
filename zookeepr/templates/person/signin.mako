<%inherit file="/base.mako" />

<h2 class="pop">Sign in</h2>

<p>Don't have an account? ${ h.link_to('Sign up', url=h.url_for(controller='person', action='new')) } now!</p>
% if c.auth_failure == 'NO_ROLE':
    <span class="error-message">You don't have the appropriate permissions to access this resource. Please login as a different user.</span>
% endif
${ h.form(h.url_for(), method='post') }

    <p class="label"><label for="person.email_address">Email address:</label></p>
    <p class="entries">${ h.text('person.email_address', size=40) }</p>

    <p class="label"><label for="person.password">Password:</label></p>
    <p class="entries">${ h.password('person.password') }</p>

    <p class="submit">${ h.submit('Sign in', 'Sign in') }</p>

${ h.end_form() }


<p>
${ h.link_to('Forgotten your password?', url=h.url_for(controller='person', action='forgotten_password', id=None)) }<br />
If you have lost your log in details, please contact ${ h.webmaster_email() }.
</p>


<p>Note: this login is for the ${h.event_name()} website; we have not
carried over any earlier linux.conf.au login information, so you will need
to register anew.</p>

