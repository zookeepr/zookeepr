<div style="float: right; border: solid lightgray; text-align: center;
padding-top: 1em; padding-bottom: 1em; padding-left: 1em; padding-right: 1em;
margin-top: 0.5em; margin-bottom: 0.5em; ">
% if c.eb:
<b>Earlybird</b> is available.<br/><br/><% c.ebtext |h%>
% else:
<b>Earlybird no longer available</b>.<br/><br/><% c.ebtext |h%>
% #endif
</div>
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
% elif not hasattr(c.signed_in_person, 'registration') or c.signed_in_person.registration==None:
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

<h3>Other option</h3>

<p><a href="/registration/<% c.signed_in_person.registration.id %>/edit"
>Edit details</a></p>

<h3>Summary of steps</h3>
&#9745; Fill in registration form
<br/>&#9744; Generate invoice
<br/>&#9744; Pay
<br/>&#9744; Attend conference
% elif c.signed_in_person.invoices[0].paid():
<p><b>Registered and paid.</b></p>

<h3>Next step</h3>

<p>Attend conference.</p>

<h3>Other options</h3>

<p>
%   if not c.signed_in_person.invoices[0].good_payments:
<a href="/registration/<% c.signed_in_person.registration.id %>/edit"
>Edit details</a><br/>
<a href="/registration/<% c.signed_in_person.registration.id %>/pay"
>Regenerate invoice</a><br/>
%   else:
<a href="/registration/<% c.signed_in_person.registration.id %>"
>View details</a><br/>
%   #endif
<a href="/invoice/<% c.signed_in_person.invoices[0].id %>" >View
invoice</a><br/>
<a href="/invoice/<% c.signed_in_person.invoices[0].id %>/printable" >View
printable invoice</a></p>

<h3>Summary of steps</h3>
&#9745; Fill in registration form
<br/>&#9745; Generate invoice
<br/>&#9745; Pay
<br/>&#9744; Attend conference
% elif c.signed_in_person.invoices[0].bad_payments:
<p><b>Tentatively registered and tried to pay.</b></p>

<p>Unfortunately, there was some sort of problem with your payment.</p>

<h3>Next step</h3>

<p><% h.contact_email('Contact the committee') %></p>

<p>Your details are:
person <% c.signed_in_person.id %>,
registration <% c.signed_in_person.registration.id %>, 
invoice <% c.signed_in_person.invoices[0].id %>.</p>

<h3>Other option</h3>
<a href="/registration/<% c.signed_in_person.registration.id %>"
>View registration details</a><br/>

<h3>Summary of steps</h3>
&#9745; Fill in registration form
<br/>&#9745; Generate invoice
<br/>&#9744; Pay
<br/>&#9744; Attend conference
% else:
<p><b>Tentatively registered.</b></p>

<h3>Next step</h3>

<p><a href="/invoice/<% c.signed_in_person.invoices[0].id %>/pay" >Pay your
registration</a></p>

<h3>Other options</h3>

<p><a href="/registration/<% c.signed_in_person.registration.id %>/edit"
>Edit details</a>
<br/><a href="/registration/<% c.signed_in_person.registration.id %>/pay"
>Regenerate invoice</a>
<br/><a href="/invoice/<% c.signed_in_person.invoices[0].id %>" >View
invoice</a>
<br/><a href="/invoice/<% c.signed_in_person.invoices[0].id %>/printable" >View
printable invoice</a></p>

<h3>Summary of steps</h3>
&#9745; Fill in registration form
<br/>&#9745; Generate invoice
<br/>&#9744; Pay
<br/>&#9744; Attend conference
% #endif
