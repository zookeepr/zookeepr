<%inherit file="/base.mako" />

<h2 class="pop">Sign in</h2>

% if c.auth_failure == 'NO_ROLE':
    <span class="error-message">You don't have the appropriate permissions to access this resource. Please login as a different user.</span>
% endif

${ h.form('/person/persona_login', method='post', id='persona-form') }
${ h.hidden('assertion', '') }
${ h.end_form() }

<form novalidate="true" action="/person/signin" method="post" data-toggle="validator">
    <div class="form-group">
        <label for="personemail_address">Email</label>
      <div class="input-group">
        <input id="personemail_address" class="form-control" placeholder="Email Address" name="person.email_address" data-error="Uh Oh, that email address doesn't look right" value="" type="email">
        <span class="input-group-addon" id="basic-addon2">required</span>
      </div>
      <div class="help-block with-errors"></div>
    </div>
    <div class="form-group">
        <label for="personpassword">Password</label> <a href="/person/forgotten_password">(forgot password)</a>
      <div class="input-group">
        <input id="personpassword" class="form-control" placeholder="Password" name="person.password" value="" type="password">
        <span class="input-group-addon" id="basic-addon2">Min. 8 Char</span>
      </div>
    </div>
  <div class="form-group">
    <button style="pointer-events: all; cursor: pointer;" type="submit" class="btn btn-primary disabled">Sign in</button>
    <a class="btn btn-default" role="button" href="/person/new">Sign up</a>
    <a class="btn btn-link persona-button" role="button" href="javascript:login()">Sign in with Persona</a>
  </div>
</form>

<p>
If you have lost your log in details, please contact ${ h.email_link_to(c.config.get('webmaster_email')) }.
</p>


<p>Note: this login is for the ${ c.config.get('event_name') } website; we have not
carried over any earlier login information, so you will need
to register anew.</p>

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
