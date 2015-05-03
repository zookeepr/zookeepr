    <div class="form-group">
      <div class="input-group">
        <input type="text" id="personfirstname" class="form-control" placeholder="First Name" name="person.firstname" />
        <span class="input-group-addon" id="basic-addon2">required</span>
      </div>
    </div>

    <div class="form-group">
      <div class="input-group">
        <input type="text" id="personlastname" class="form-control" placeholder="Last Name" name="person.lastname" required />
        <span class="input-group-addon" id="basic-addon2">required</span>
      </div>
    </div>

${ h.hidden('person.company', value='') }</p>

% if c.form is not 'edit' or h.auth.authorized(h.auth.has_organiser_role):
    <div class="form-group">
      <div class="input-group">
        <input type="email" id="personemail_address" class="form-control" placeholder="Email Address" name="person.email_address" data-error="Uh Oh, that email address doesn't look right" />
        <span class="input-group-addon" id="basic-addon2">required</span>
      </div>
      <div class="help-block with-errors"></div>
    </div>
% else:
    <div class="form-group">
      <div class="input-group">
        <div class="input-group">
          <input type="email" id="personemail_address" class="form-control" name="person.email_address" readonly />
          <span class="input-group-addon" id="basic-addon2">required</span>
        </div>
        <p class="help-block">We would like to avoid the changing of email addresses, however if you require your account email address to be updated, please email <a href="mailto:contact@lcabythebay.org.au">contact@lcabythebay.org.au</a></p>
      </div>
    </div>
% endif

% if c.form is not 'edit': 
    <div class="form-group">
      <div class="input-group">
        <input type="password" id="personpassword" class="form-control" placeholder="Password" name="person.password" />
        <span class="input-group-addon" id="basic-addon2">Min. 8 Char</span>
      </div>
    </div>

    <div class="form-group">
      <div class="input-group">
        <input type="password" id="personpassword_confirm" class="form-control" placeholder="Confirm" name="person.password_confirm" data-match="#personpassword" data-match-error="Whoops, these don't match" required/>
        <span class="input-group-addon" id="basic-addon2">Must Match</span>
      </div>
      <div class="help-block with-errors"></div>
    </div>
% endif
<br />
%if c.config.get('personal_info')['phone'] == 'yes':
    <div class="form-group">
      <div class="input-group">
        <input type="text" id="personphone" class="form-control" placeholder="Phone Number" name="person.phone" required />
        <span class="input-group-addon" id="basic-addon2">required</span>
      </div>
      <div class="help-block with-errors"></div>
    </div>
%else:
${ h.hidden('person.phone') }
${ h.hidden('person.mobile') }
%endif

%if c.config.get('personal_info')['home_address'] == 'yes':
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

    <div class="form-group">
      <div class="input-group">
        <select id="personcountry" class="form-control" placeholder="Country" name="person.country">
%for country in h.countries():
% if country == 'australia':
          <option selected="selected" value="${ country }">${ country }</option>
% else:
          <option value="${ country }">${ country }</option>
% endif
%endfor
        </select>
      </div>
    </div>


%if False and c.social_networks:
<p class="label">Your <b>username</b> on social networking sites:
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
</p>
%endif

%if not c.person or not c.person.i_agree:
  <div class="form-group">
    <div class="checkbox">
      <label>
        <input type="checkbox" name="person.i_agree" id="personi_agree" data-error="An account cannot be created if you don't agree with the T&Cs" required>
        I agree to the <a href="/cor/terms_and_conditions" target="_blank">terms and conditions</a>
      </label>
      <div class="help-block with-errors"></div>
    </div>
  </div>
%else:
<p>${ h.yesno(True) |n } <label for="personi_agree">I agree to the</label> <a href="/cor/terms_and_conditions" target="_blank">conditions of registration</a></p>
${ h.hidden('person.i_agree', True) }
%endif
