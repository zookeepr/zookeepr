<%inherit file="/base.mako" />
<h2>Finish Sign up</h2>

<p>Before, you do anything else, please take the time to add the following details to your account:</p>

${ h.form(h.url_for(id=c.person.id)) }

%if not c.person.firstname:
<p class="label"><span class="mandatory">*</span><label for="person.firstname">Your first name:</label></p>
<p class="entries">${ h.text('person.firstname', size=40) }</p>
%else:
${ h.hidden('person.firstname') }
%endif

%if not c.person.lastname:
<p class="label"><span class="mandatory">*</span><label for="person.lastname">Your last name:</label></p>
<p class="entries">${ h.text('person.lastname', size=40) }</p>
%else:
${ h.hidden('person.lastname') }
%endif

${ h.hidden('person.email_address') }
${ h.hidden('person.company') }

%if not c.person.mobile and c.mobile_is_mandatory:
<p class="label"><span class="mandatory">*</span>
<label for="person.mobile">Mobile/Cell number:</label></p>
<p class="entries">${ h.text('person.mobile') }</p>
%else:
${ h.hidden('person.mobile') }
%endif

${ h.hidden('person.phone') }

%if (not c.person.address1 or not c.person.city or not c.person.postcode) and c.config.get('personal_info', category='rego')['home_address'] == 'yes':
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
%else:
${ h.hidden('person.address1') }
${ h.hidden('person.address2') }
${ h.hidden('person.city') }
${ h.hidden('person.state') }
${ h.hidden('person.postcode') }
%endif

%if not c.person.country:
<p class="label"><span class="mandatory">*</span><label for="person.country">Country:</label></p>
<p class="entries">
${ h.select('person.country', None, h.countries()) }
</p>
%else:
${ h.hidden('person.country') }
%endif

%if not c.person.i_agree:
<p>${ h.checkbox('person.i_agree') } <label for="personi_agree">I agree to the</label> <a href="/cor/terms_and_conditions" target="_blank">conditions of registration</a></p>
%else:
${ h.hidden('person.i_agree') }
%endif

<p>${ h.submit('update', 'Save') }</p>

${ h.end_form() }
