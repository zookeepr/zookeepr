<p class="label"><span class="mandatory">*</span><label for="person.firstname">Your first name:</label></p>
<p class="entries">${ h.text('person.firstname', size=40) }</p>

<p class="label"><span class="mandatory">*</span><label for="person.lastname">Your last name:</label></p>
<p class="entries">${ h.text('person.lastname', size=40) }</p>

<p class="label"><label for="person.company">Company:</label></p>
<p class="entries">${ h.text('person.company', size=40) }</p>

% if c.form is not 'edit' or h.auth.authorized(h.auth.has_organiser_role):
<p class="label"><span class="mandatory">*</span><label for="person.email_address">Email address:</label></p>
<p class="entries">${ h.text('person.email_address', size=40) }</p>
%   if c.form is not 'edit':
<p class="label"><span class="mandatory">*</span><label for="person.email_address2">Confirm your email address:</label></p>
<p class="entries">${ h.text('person.email_address2', size=40) }</p>
%   endif
% else:
${ h.hidden('person.email_address', '') }</p>
${ h.hidden('person.email_address2', '') }</p>
% endif

% if c.form is not 'edit':
<p class="label"><span class="mandatory">*</span><label for="person.password">Choose a password:</label></p>
<p class="entries">${ h.password("person.password", size=40) }</p>

<p class="label"><span class="mandatory">*</span><label for="person.password_confirm">Confirm your password:</label></p>
<p class="entries">${ h.password("person.password_confirm", size=40) }</p>
% endif

<p><label for="person.phone">Phone number</label></p>
<p class="entries">${ h.text('person.phone') }</p>

% if c.mobile_is_mandatory:
<p class="label"><span class="mandatory">*</span>
% else:
<p>
% endif
<label for="person.mobile">Mobile/Cell number</label></p>
<p class="entries">${ h.text('person.mobile') }</p>

<p class="label"><span class="mandatory">*</span><label for="person.address">Address:</label></p>
<p class="entries">
${ h.text('person.address1', size=40) }
<br>
${ h.text('person.address2', size=40) }
</p>

<p class="label"><span class="mandatory">*</span><label for="person.city">City/Suburb:</label></p>
<p class="entries">${ h.text('person.city', size=40) }</p>

<p class="label"><label for="person.state">State/Province:</label></p>
<p class="entries">${ h.text('person.state', size=40) }</p>

<p class="label"><span class="mandatory">*</span><label for="person.postcode">Postcode/ZIP:</label></p>
<p class="entries">${ h.text('person.postcode', size=40) }</p>

<p class="label"><span class="mandatory">*</span><label for="person.country">Country:</label></p>
<p class="entries">
${ h.select('person.country', None, h.countries()) }
</p>

<table>
% for network in c.social_networks:
  <tr class="${ h.cycle('even', 'odd') }">
    <td><img style="padding-right: 5px" src="/images/${ network.logo }">${ network.name }</td>
%   if c.person:
    <td>${ h.hidden('social_network-%s.name' % network.id, value=network.name) }${ h.text('social_network-%s.account_name' % network.id, value=c.person.social_network[network.name]) }</td>
%   else:
    <td>${ h.hidden('social_network-%s.name' % network.id, value=network.name) }${ h.text('social_network-%s.account_name' % network.id, value='') }</td>
%   endif
  </tr>
% endfor
</table>
  

