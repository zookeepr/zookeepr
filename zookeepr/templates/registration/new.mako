    <%inherit file="/base.mako" />

<% desc, descChecksum = h.silly_description() %>

    <h2>Register for ${ h.event_name() }</h2>
    <div id="registration">
% if not 'conference' in c.ceilings or c.ceilings['conference'].available(): 
      <p>Welcome to the registration form for ${ h.event_name() }. Please fill in the form as best you can.</p>
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

% if not h.signed_in_person():
      <p>If you already have an account (through a submitting a proposal, or other interaction with this site), then please ${ h.link_to('sign in', url=h.url_for(controller='person', action='signin')) }.</p>
      <p>If you can't log in, you can try ${ h.link_to('recovering your password', url=h.url_for(controller='person', action='forgotten_password')) }.</p>
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

<%include file="form.mako" />

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
