    <%inherit file="/base.mako" />

<% desc, descChecksum = h.silly_description() %>

% if not 'conference-paid' in c.ceilings or c.ceilings['conference-paid'].available(): 
%   if c.special_offer is not None:
    <h2>Register for ${ c.config.get('event_name') } (${ c.special_offer.name } Special Offer)</h2>
    <div id="registration">
${ c.special_offer.description | n }
%   else:
    <h2>Register for ${ c.config.get('event_name') }</h2>
    <div id="registration">
      <p>Welcome to the registration form for ${ c.config.get('event_name') }. Please fill in the form as best you can.</p>
%   endif
% else:
      <p class="error-message"><i>Registration is closed.</i></p>
      <p class="error-message">
        Please only use this form:
        <ul class="error-message">
          <li>to volunteer to help at the conference, or</li>
          <li>to buy dinner tickets, or</li>
          <li>if you are have a voucher code or similar.</li>
        </ul>
      </p>
% endif

% if errors:
      <p class="error-message">There
%   if len(errors)==1:
      is one problem
%   else:
      are ${ `len(errors)` |h } problems
%   endif
      with your registration form, highlighted in red below. Please correct and re-submit.</p>
% endif

      ${ h.form(h.url_for()) }
%if c.special_offer is not None:
        ${ h.hidden('special_offer.name', c.special_offer.name) }
        <p class="label"><span class="mandatory">*</span><label for="special_offermember_number">${ c.special_offer.id_name }:</label></p>
        <p class="entries">${ h.text('special_offer.member_number', size=40) }</p>
%else:
        ${ h.hidden('special_offer.name', '') }
        ${ h.hidden('special_offer.member_number', '') }
%endif

<%include file="form.mako" />

%if not c.signed_in_person.i_agree:
        <p>${ h.checkbox('person.i_agree') } <label for="personi_agree">I agree to the</label> <a href="/cor/terms_and_conditions" target="_blank">terms and conditions</a></p>
%else:
        <p>${ h.yesno(True) |n } I agree to the <a href="/cor/terms_and_conditions" target="_blank">terms and conditions</a></p>
        ${ h.hidden('person.i_agree', True) }
%endif
        <p class="submit">${ h.submit("submit", "Register me!") }</p>
        <p><span class="fielddesc">If you encounter any problems signing up please email ${ h.email_link_to(c.config.get('contact_email')) }.</span></p>

      ${ h.end_form() }
      </div>

<%def name="short_title()"><%
  return "Registration"
%></%def>
<%def name="title()" >
Register - ${ parent.title() }
</%def>
