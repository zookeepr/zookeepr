<%inherit file="/base.mako" />

<h2 class="pop">Sign in</h2>

<p>Don't have an account? ${ h.link_to('Sign up', url=h.url_for(controller='person', action='new')) } now!</p>
% if c.auth_failure == 'NO_USER' or c.auth_failure == 'BAD_PASSWORD':
    <span class="error-message">Your sign-in details are incorrect; try the 'Forgotten your password' link below or sign up for a new person.</span>
% elif c.auth_failure == 'NOT_ACTIVATED':
    <span class="error-message">You haven't yet confirmed your registration, please refer to your email for instructions on how to do so.</span>
% elif c.auth_failure == 'NO_ROLE':
    <span class="error-message">You don't have the appropriate permissions to access this resource. Please login as a different user.</span>
% endif
${ h.form('FORM_ACTION') }

    <p class="label"><label for="username">Email address:</label></p>
    <p class="entries">${ h.text('username', size=40) }</p>

    <p class="label"><label for="password">Password:</label></p>
    <p class="entries">${ h.password('password') }</p>

    <p class="submit">${ h.submit('Sign in', 'Sign in') }</p>

${ h.end_form() }


<p>
${ h.link_to('Forgotten your password?', url=h.url_for(controller='person', action='forgotten_password')) }<br />
If you have lost your log in details, please contact ${ h.webmaster_email() }.
</p>


<p>Note: this login is for the 2009 linux.conf.au website; we have not
carried over any earlier linux.conf.au login information, so you will need
to register anew.</p>

