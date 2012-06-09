<%inherit file="/base.mako" />

<h2 class="pop">Sign in</h2>

% if c.auth_failure == 'NO_ROLE':
    <span class="error-message">You don't have the appropriate permissions to access this resource. Please login as a different user.</span>
% endif

<div id="persona-div" style="display: none">
<p>Don't want yet another single-use username/password?

<p><a href="javascript:login()"><img border="0" src="/images/persona-login.png" alt="Sign in with Persona"></a></p>

${ h.form('/person/persona_login', method='post', id='persona-form') }
${ h.hidden('assertion', '') }
${ h.end_form() }

<p>Otherwise enter your credentials in the following form.</p>
</div>

${ h.form(h.url_for(), method='post') }

    <p class="label"><label for="person.email_address">Email address:</label></p>
    <p class="entries">${ h.text('person.email_address', size=40) }</p>

    <p class="label"><label for="person.password">Password:</label></p>
    <p class="entries">${ h.password('person.password') }</p>

    <p class="submit">${ h.submit('Sign in', 'Sign in') }</p>

${ h.end_form() }

<p>Don't have an account? ${ h.link_to('Sign up', url=h.url_for(controller='person', action='new')) } now!</p>

<p>
${ h.link_to('Forgotten your password?', url=h.url_for(controller='person', action='forgotten_password', id=None)) }<br />
If you have lost your log in details, please contact ${ h.webmaster_email() }.
</p>


<p>Note: this login is for the ${h.event_name()} website; we have not
carried over any earlier login information, so you will need
to register anew.</p>

<script src="https://browserid.org/include.js"></script>
<script>
var persona_div = document.getElementById("persona-div");
persona_div.style.display = 'inline';

function login() {
    navigator.id.get(function (assertion) {
      if (assertion) {
        var assertion_field = document.getElementById("assertion");
        assertion_field.value = assertion;

        var login_form = document.getElementById("persona-form");
        login_form.submit();
      }
    });
}
</script>
