<h3>Register for the conference</h3>

<p>
Welcome to the conference registration. Please fill in the form as best you can. 
</p>

% if not 'signed_in_person_id' in session:
<p>
If you already have an account (through a prior registration, or other interaction with this site), then please sign in.
</p>
<p>If you can't log in, you can try
<% h.link_to('recovering your password', url=h.url(controller='account', action='forgotten_password', id=None)) %>.
</p>
% #endif

<&| @zookeepr.lib.form:fill, defaults=defaults, errors=errors &>
<% h.form(h.url()) %>

<fieldset id="person">
<h4>Account details</h4>

% if not c.signed_in_person:
<p>
<span class="mandatory">*</span> - Mandatory field
</p>
% #endif

<p>
% if not c.signed_in_person:
<span class="mandatory">*</span>
% #endif
<label for="person.fullname">Your full name:</label>
% if c.signed_in_person:
<% c.signed_in_person.fullname | h %>
% else:
<br />
<% h.text_field('person.fullname', size=40) %>
% #endif
</p>

<p>
% if not c.signed_in_person:
<span class="mandatory">*</span>
% #endif
<label for="person.email_address">Email address:</label>
% if c.signed_in_person:
<% c.signed_in_person.email_address | h %>
% else:
<br />
<% h.text_field('person.email_address', size=40) %>
% #endif
<br />
<span class="fielddesc">
Your email address will only be used to correspond with you, and is your login name for the website.  It will not be shown or used otherwise.
</span>
</p>

% if not c.signed_in_person:
<p>
<span class="mandatory">*</span>
<label for="person.password">Choose a password:</label>
<br />
<% h.password_field("person.password", size=40) %>
</p>

<p>
<span class="mandatory">*</span>
<label for="person.password_confirm">Confirm your password:</label>
<br />
<% h.password_field("person.password_confirm", size=40) %>
</p>
% #endif

<p>
% if not c.signed_in_person:
<span class="mandatory">*</span>
% #endif
<label for="person.handle">Display name/handle/nickname:</label>
% if c.signed_in_person:
<% c.signed_in_person.handle |h %>
% else:
<br />
<% h.text_field('person.handle', size=40) %>
% #endif
<br />
<span class="fielddesc">
Your display name will be used to identify you on the website.
</span>
</p>
</fieldset>

<& form.myt &>

<% h.submit("Register me!") %>
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
	defaults = {'registration.checkout': '20',
		'registration.lasignup': '1',
		'registration.announcesignup': '1',
		'registration.dinner': '0',
		}
</%init>

