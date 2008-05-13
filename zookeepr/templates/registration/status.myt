<div style="float: right; border: solid lightgray; text-align: center;
padding-top: 1em; padding-bottom: 1em; padding-left: 1em; padding-right: 1em;
margin-top: 0.5em; margin-bottom: 0.5em; ">
% if c.ceiling.open:
<b>Registrations</b> are open<br/><br/>
% else:
<b>Registrations are closed</b><br/><br/>
% #endif
<% c.ceiling.text %><br/><br/>
% if c.eb:
<b>Earlybird</b> is available<br/><br/><% c.ebtext |h%>
% else:
<b>Earlybird no longer available</b><br/><br/><% c.ebtext |h%>
% #endif
</div>
% if c.ceiling.open:
<h2>Your registration status</h2>
% else:
<h2>Registrations are closed</h2>
<p>Registrations are now closed. You will only be able to register if you
have an existing voucher code or if you're otherwise entitled to attend
for free (eg speakers).</p>
<h3>Your registration status</h3>
% #endif

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
% elif c.signed_in_person.registration.type=='Volunteer' and not c.signed_in_person.registration.volunteer:
<p><b>Tentatively volunteered.</b></p>

<h3>Next step</h3>

<p><a href="/registration/<% c.signed_in_person.registration.id %>/volunteer"
>Select areas of interest and ability</a></p>

<h3>Other option</h3>

<p><a href="/registration/<% c.signed_in_person.registration.id %>/edit"
>Edit details</a></p>

<h3>Summary of steps</h3>
&#9745; Fill in registration form
%   if c.signed_in_person.invoices and c.signed_in_person.invoices[0].paid():
<br/>&#9745; Generate invoice
<br/>&#9745; Pay
%   else:
<br/>&#9744; Generate invoice
<br/>&#9744; Pay
%   #endif
<br/>&#9744; Attend conference
% elif not c.signed_in_person.invoices:
<p><b>Tentatively registered.</b></p>

<h3>Next step</h3>

<p><a href="/registration/<% c.signed_in_person.registration.id %>/pay"
>Generate invoice</a></p>

<h3>Other option</h3>

<p><a href="/registration/<% c.signed_in_person.registration.id %>/edit"
>Edit details</a>
%   if c.signed_in_person.registration.type=='Volunteer':
<br/><a href="/registration/<% c.signed_in_person.registration.id %>/volunteer"
>Change areas of interest and ability</a>
%   #endif
</p>

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
%   if c.signed_in_person.registration.type=='Volunteer':
<a href="/registration/<% c.signed_in_person.registration.id %>/volunteer"
>Change areas of interest and ability</a><br/>
%   #endif
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
printable invoice (html)</a><br/>
<a href="/invoice/<% c.signed_in_person.invoices[0].id %>.pdf" >Get
printable invoice (pdf)</a></p>

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
printable invoice (html)</a>
<br/><a href="/invoice/<% c.signed_in_person.invoices[0].id %>.pdf" >View
printable invoice (pdf)</a></p>

<h3>Summary of steps</h3>
&#9745; Fill in registration form
<br/>&#9745; Generate invoice
<br/>&#9744; Pay
<br/>&#9744; Attend conference
% #endif
