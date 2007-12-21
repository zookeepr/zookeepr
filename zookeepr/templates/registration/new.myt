<h2>Register for the conference</h2>

#<p>
#Welcome to the conference registration. Please fill in the form as best you can.
#</p>
<p class="error-message"><b>Registration is closed.</b>
Please only fill in this form if you are have a discount code or similar.
</p>

% if not 'signed_in_person_id' in session:
<p>
If you already have an account (through a prior registration, or other
interaction with this site), then please <a href="/account/signin">sign in</a>.
</p>
<p>If you can't log in, you can try
<% h.link_to('recovering your password', url=h.url(controller='account', action='forgotten_password', id=None)) %>.
</p>
% #endif

% if errors:
<p class="error-message">There
%   if len(errors)==1:
is one problem
%   else:
are <% `len(errors)` |h %> problems
%   #endif
with your registration form, highlighted in red below. Please correct and
re-submit.</p>
% #endif

<&| @zookeepr.lib.form:fill, defaults=defaults, errors=errors &>
<% h.form(h.url()) %>

<fieldset id="person">
<h2>About yourself</h2>

% if not c.signed_in_person:
<br><p class="note">
<span class="mandatory">*</span> - Mandatory field
</p>
% #endif

<p class="label">
% if not c.signed_in_person:
<span class="mandatory">*</span>
% #endif
<label for="person.firstname">Your first name:</label></p>
% if c.signed_in_person:
<p>
<% c.signed_in_person.firstname | h %>
% else:
<p class="entries">
<% h.text_field('person.firstname', size=40) %>
% #endif
</p>

<p class="label">
% if not c.signed_in_person:
<span class="mandatory">*</span>
% #endif
<label for="person.lastname">Your last name:</label></p>
% if c.signed_in_person:
<p>
<% c.signed_in_person.lastname | h %>
% else:
<p class="entries">
<% h.text_field('person.lastname', size=40) %>
% #endif
</p>


<p class="label">
% if not c.signed_in_person:
<span class="mandatory">*</span>
% #endif
<label for="person.email_address">Email address:</label></p>
% if c.signed_in_person:
<p>
<% c.signed_in_person.email_address | h %>
% else:
<p class="entries">
<% h.text_field('person.email_address', size=40) %>
% #endif
</p>
<p class="note">
Your email address will only be used to correspond with you, and is your login name for the website.  It will not be shown or used otherwise.
</p>

% if not c.signed_in_person:
<p class="label">
<span class="mandatory">*</span>
<label for="person.password">Choose a password:</label>
</p><p class="entries">
<% h.password_field("person.password", size=40) %>
</p>

<p class="label">
<span class="mandatory">*</span>
<label for="person.password_confirm">Confirm your password:</label>
</p><p class="entries">
<% h.password_field("person.password_confirm", size=40) %>
</p>
% #endif

<p class="label">
% if not c.signed_in_person:
<span class="mandatory">*</span>
% #endif
<label for="person.handle">Display name/handle/nickname:</label></p>
% if c.signed_in_person:
<p>
<% c.signed_in_person.handle |h %>
% else:
<p class="entries">
<% h.text_field('person.handle', size=40) %>
% #endif
</p>
<p class="note">
Your display name will be used to identify you on the website. It's not
actually used for much. For an IRC nick or handle to be shown on the badge,
see "superhero name" below.
</p>
</fieldset>

<& form.myt &>

<p class="submit"><% h.submit("Register me!") %></p>
<span class="fielddesc">
If you encounter any problems signing up please email <% h.contact_email() %>
</span>


<% h.end_form() %>
</&>

<%args>
defaults
errors
</%args>

<%init>
# work around bug in formencode, set defaults
if not defaults:
	defaults = {'registration.checkout': '2',
		'registration.lasignup': '1',
		'registration.announcesignup': '1',
		'registration.dinner': '0',
		'registration.speaker_record': '1',
		'registration.speaker_video_release': '1',
		'registration.speaker_slides_release': '1',
		}
</%init>
