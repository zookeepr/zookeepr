    <h2>Register for the conference</h2>
    <div id="registration">
% if c.ceilings['conference'].available(): 
      <p>Welcome to the conference registration. Please fill in the form as best you can.</p>
% else:
      <p class="error-message"><i>Registration is closed.</i></p>
      <p class="error-message">
        Please only use this form:
        <ul class="error-message">
          <li>to volunteer to help at the conference, or</li>
          <li>to buy the Monday, Tuesday or Penguin Dinner tickets, or</li>
          <li>if you are have a voucher code or similar.</li>
        </ul>
      </p>
% #endif

% if not 'signed_in_person_id' in session:
      <p>If you already have an account (through a submitting a proposal, or other interaction with this site), then please <a href="/person/signin">sign in</a>.</p>
      <p>If you can't log in, you can try <% h.link_to('recovering your password', url=h.url(controller='person', action='forgotten_password', id=None)) %>.</p>
% #endif

% if errors:
      <p class="error-message">There
%   if len(errors)==1:
      is one problem
%   else:
      are <% `len(errors)` |h %> problems
%   #endif
      with your registration form, highlighted in red below. Please correct and re-submit.</p>
% #endif

      <&| @zookeepr.lib.form:fill, defaults=defaults, errors=errors &>
      <% h.form(h.url()) %>

<& form.myt, defaults=defaults, errors=errors &>

        <p class="submit"><% h.submitbutton("Register me!") %></p>
        <p><span class="fielddesc">If you encounter any problems signing up please email <% h.contact_email() %>.</span></p>

      <% h.end_form() %>
      </&>
      </div>

<%args>
defaults
errors
</%args>

<%init>
# work around bug in formencode, set defaults
if not defaults:
    desc, descChecksum = h.silly_description()

    defaults = {'person.country': 'Australia',
        'registration.checkout': '24',
        'registration.lasignup': '1',
        'registration.announcesignup': '1',
        'registration.dinner': '0',
        'registration.speaker_record': '1',
        'registration.speaker_video_release': '1',
        'registration.speaker_slides_release': '1',
        'registration.shell': '',
        'registration.editor': '',
        'registration.distro': '',
        'registration.silly_description': desc,
        'registration.silly_description_checksum': descChecksum,
    }
    if c.signed_in_person:
        for k in ['address1', 'address2', 'city', 'state', 'postcode', 'country', 'phone', 'mobile', 'company']:
            v = getattr(c.signed_in_person, k)
            if v is not None:
                defaults['person.' + k] = getattr(c.signed_in_person, k)


</%init>

<%method title>
Register - <& PARENT:title &>
</%method>

<%method extra_head>
  
</%method>
