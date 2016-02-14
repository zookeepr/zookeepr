<%inherit file="/base.mako" />
        <h3>Forgotten password?</h3>

<p>If you don't want to have to remember a password just for this site, you can simply login with Persona and forget about resetting your forgotten password.</p>

<p><a class="persona-button" href="javascript:login()"><span>Sign in with Persona</span
></a></p>

${ h.form('/person/persona_login', method='post', id='persona-form') }
${ h.hidden('assertion', '') }
${ h.end_form() }

        <p>Otherwise, here's how the password reset works.</p>
	${ h.form( h.url_for(), method='post', id='pwreset-form') }
        <p>
            Enter your email address and an email will be sent to you allowing you to
            select a new password.
        </p>
        <div class="centre">
            <p class="label"><span class="mandatory">*</span>Email address:</p>
            <p class="entries">${ h.text('email_address', size=60) }</p>
            <p class="submit">${ h.submit('submit', 'Set a new password') }</p>
        </div>
${ h.end_form() }

<%def name="title()">
Forgotten Password? -
 ${ parent.title() }
</%def>

<script src="https://login.persona.org/include.js"></script>
<script>
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
<%def name="extra_head()">
<link rel="stylesheet" href="/css/persona.css" type="text/css">
</%def>
