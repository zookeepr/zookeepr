<%inherit file="/base.mako" />
<h2 class="featurette-heading">Finish Sign up</h2>

<p class="lead">Before, you do anything else, please take the time to add the following details to your account:</p>

<form action="/person/${ c.person.id }/finish_signup" method="post" data-toggle="validator">

%if not c.person.firstname:
    <div class="form-group">
      <div class="input-group">
        <input type="text" id="personfirstname" class="form-control" placeholder="First Name" name="person.firstname" />
        <span class="input-group-addon" id="basic-addon2">required</span>
      </div>
    </div>
%else:
${ h.hidden('person.firstname') }
%endif

%if not c.person.lastname:
    <div class="form-group">
      <div class="input-group">
        <input type="text" id="personlastname" class="form-control" placeholder="Last Name" name="person.lastname" required />
        <span class="input-group-addon" id="basic-addon2">required</span>
      </div>
    </div>
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
    <div class="form-group">
      <div class="input-group">
        <input type="text" id="personaddress1" class="form-control" placeholder="Address" name="person.address1" required />
        <span class="input-group-addon" id="basic-addon2">required</span>
      </div>
      <div class="help-block with-errors"></div>
    </div>
    <div class="form-group">
        <input type="text" id="personaddress2" class="form-control" placeholder="Additional Address" name="person.address2" />
    </div>

    <div class="form-group">
      <div class="input-group">
        <input type="text" id="personcity" class="form-control" placeholder="City/Suburb" name="person.city" required />
        <span class="input-group-addon" id="basic-addon2">required</span>
      </div>
      <div class="help-block with-errors"></div>
    </div>

    <div class="form-group">
        <input type="text" id="personstate" class="form-control" placeholder="State" name="person.state" />
    </div>

    <div class="form-group">
      <div class="input-group">
        <input type="text" id="personpostcode" class="form-control" placeholder="Postcode/ZIP" name="person.postcode" required />
        <span class="input-group-addon" id="basic-addon2">required</span>
      </div>
      <div class="help-block with-errors"></div>
    </div>
%else:
${ h.hidden('person.address1') }
${ h.hidden('person.address2') }
${ h.hidden('person.city') }
${ h.hidden('person.state') }
${ h.hidden('person.postcode') }
%endif

%if not c.person.country:
    <div class="form-group">
      <div class="input-group">
        <select id="personcountry" class="form-control" placeholder="Country" name="person.country" value="AUSTRALIA">
%  for country in h.countries():
          <option>${ country }</option>
%  endfor
        </select>
      </div>
    </div>
%else:
${ h.hidden('person.country') }
%endif

%if not c.person.i_agree:
  <div class="form-group">
    <div class="checkbox">
      <label>
        <input type="checkbox" name="person.i_agree" id="personi_agree" data-error="An account cannot be created if you don't agree with the T&Cs" required>
        I agree to the <a href="/cor/terms_and_conditions" target="_blank">conditions of registration</a>
      </label>
      <div class="help-block with-errors"></div>
    </div>
  </div>
%else:
${ h.hidden('person.i_agree') }
%endif

  <div class="form-group">
    <button type="submit" class="btn btn-primary">Finish account creation</button>
  </div>

${ h.end_form() }
