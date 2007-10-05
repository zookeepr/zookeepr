<h2>Your registration status</h2>

% if not 'signed_in_person_id' in session:
<p><b>Not signed in or not registered.</b></p>

<h3>Next step</h3>

<p><a href="/account/signin">Sign in</a> if you already have an account
(you've already registered, submitted a paper or similar).  If you can't
log in, you can try <% h.link_to('recovering your password',
url=h.url(controller='account', action='forgotten_password', id=None)) %>.</p>
%   session['sign_in_redirect'] = '/registration/status'
%   session.save()

<p><a href="/registration/new">Go directly to the registration form</a>
otherwise.</p>

<h3>Summary of steps</h3>
&#9744; Fill in registration form
<br/>&#9744; Generate invoice
<br/>&#9744; Pay
<br/>&#9744; Attend conference
% elif not hasattr(c.signed_in_person, 'registration'):
<p><b>Not registered.</b>

<h3>Next step</h3>

<p><a href="/registration/new">Fill in registration form</a>.</p>

<h3>Summary of steps</h3>
&#9744; Fill in registration form
<br/>&#9744; Generate invoice
<br/>&#9744; Pay
<br/>&#9744; Attend conference
% elif not c.signed_in_person.invoices:
<p><b>Tentatively registered.</b></p>

<h3>Next step</h3>

<p><a href="/registration/<% c.signed_in_person.registration.id %>/pay"
>Generate invoice</a></p>

<h3>Alternate step</h3>

<p><a href="/registration/<% c.signed_in_person.registration.id %>/edit"
>Edit details</a></p>

<h3>Summary of steps</h3>
&#9745; Fill in registration form
<br/>&#9744; Generate invoice
<br/>&#9744; Pay
<br/>&#9744; Attend conference
% elif c.signed_in_person.invoices[0].good_payments:
<p><b>Registered and paid.</b></p>

<h3>Next step</h3>

<p>Attend conference.</p>

<h3>Summary of steps</h3>
&#9745; Fill in registration form
<br/>&#9745; Generate invoice
<br/>&#9745; Pay
<br/>&#9744; Attend conference
% elif c.signed_in_person.invoices[0].bad_payments:
<p><b>Tentatively registered and tried to pay.</b></p>

<h3>Next step</h3>

<p>Contact the committee.</p>

<h3>Summary of steps</h3>
&#9745; Fill in registration form
<br/>&#9745; Generate invoice
<br/>&#9746; Pay
<br/>&#9744; Attend conference
% else:
<p><b>Tentatively registered.</b></p>

<h3>Next step</h3>

<p><a href="/invoice/<% c.signed_in_person.invoices[0].id %>/pay" >Pay your
registration</a></p>

<h3>Alternate steps</h3>

<p><a href="/registration/<% c.signed_in_person.registration.id %>/edit"
>Edit details</a>
<br/><a href="/registration/<% c.signed_in_person.registration.id %>/pay"
>Regenerate invoice</a></p>

<h3>Summary of steps</h3>
&#9745; Fill in registration form
<br/>&#9745; Generate invoice
<br/>&#9744; Pay
<br/>&#9744; Attend conference
% #endif
