    <%inherit file="/base.mako" />

<% desc, descChecksum = h.silly_description() %>

% if not 'conference' in c.ceilings or c.ceilings['conference'].available(): 
%   if c.special_offer is not None:
    <h2>Register for ${ h.event_name() } (${ c.special_offer.name } Special Offer)</h2>
    <div id="registration">
${ c.special_offer.description | n }
%   else:
    <h2>Register for ${ h.event_name() }</h2>
    <div id="registration">
      <p>Welcome to the registration form for ${ h.event_name() }. Please fill in the form as best you can.</p>
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

        <p>${ h.checkbox('registration.i_agree') } <label for="registrationi_agree">I agree to the</label> <a href="${ h.lca_info['event_url']}/register/terms_and_conditions" target="_blank">terms and conditions</a></p>
        <p class="submit">${ h.submit("submit", "Register me!") }</p>
        <p><span class="fielddesc">If you encounter any problems signing up please email ${ h.contact_email() }.</span></p>

      ${ h.end_form() }
      </div>

<%def name="short_title()"><%
  return "Registration"
%></%def>
<%def name="title()" >
Register - ${ parent.title() }
</%def>
