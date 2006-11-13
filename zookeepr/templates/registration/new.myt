<h3>Register for the conference</h3>

<p>
Welcome to the conference registration. Please fill in the form as best you can. 
</p>

<p>
If you already have an account (through a prior registration, or other interaction with this site), then please sign in.
</p>
<p>If you can't log in, you can try
<% h.link_to('recovering your password', url=h.url(controller='account', action='forgotten_password', id=None)) %>.
</p>

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

<fieldset id="personal">

<h4>Personal Information</h4>

<p>
<span class="mandatory">*</span> - Mandatory field
</p>

<p>
<span class="mandatory">*</span>
<label for="registration.address">Address:</label>
<br />
<% h.text_field('registration.address1', size=40) %>
<br />
<% h.text_field('registration.address2', size=40) %>
<br />
<span class="mandatory">*</span>
<label for="registration.city">City/Suburb:</label>
<br />
<% h.text_field('registration.city', size=40) %>
<br />
<label for="registration.state">State/Province:</label>
<br />
<% h.text_field('registration.state', size=40) %>
<br />
<span class="mandatory">*</span>
<label for="registration.country">Country:</label>
<br />
<% h.text_field('registration.country', size=40) %>
<br />
<span class="mandatory">*</span>
<label for="registration.postcode">Postcode/ZIP:</label>
<br />
<% h.text_field('registration.postcode', size=40) %>
</p>

<p>
<label for="registration.phone">Mobile/Cell number:</label>
<br />
<% h.text_field('registration.phone') %>
</p>

<p>
<label for="registration.company">Company:</label>
#<br />
<% h.text_field('registration.company', size=60) %>
</p>

<p>
# FIXME: dynamic :)
<label for="registration.shell">Your favourite shell:</label>
<select name="registration.shell">
<option value="-">-</option>
% for s in ['zsh', 'bash', 'sh', 'csh', 'tcsh', 'emacs', 'ksh', 'smrsh', 'busybox', 'dash', 'XTree Gold']:
<option value="<%s%>"><% s %></option>
% #endfor
</SELECT>
Other: <% h.text_field('registration.shelltext') %>
</p>

<p>
<label for="registration.editor">Your favourite editor:</label>
<SELECT name="registration.editor">
<option value="-">-</option>
% for e in ['vi', 'vim', 'emacs', 'xemacs', 'gedit', 'nano', 'kate', 'jed']:
<option value="<% e %>"><% e %></option>
% #endfor
</SELECT>
Other: <% h.text_field('registration.editortext') %>
</p>

<p>
<label for="registration.distro">Your favourite distro:</label>
<SELECT name="registration.distro">
<option value="-">-</option>
% for d in ['CentOS', 'Darwin', 'Debian', 'Fedora', 'FreeBSD', 'Gentoo', 'L4', 'Mandriva', 'NetBSD', 'OpenBSD', 'OpenSolaris', 'OpenSUSE', 'RHEL', 'Slackware', 'Ubuntu']:
<option value="<% d %>"><% d %></option>
% #endfor
</SELECT>
Other: <% h.text_field('registration.distrotext') %>
</p>

<%python>
adjs1 = ["strongly",
		       "poorly", "bad	ly", "well", "dynamically",
		       "hastily", "statically", "mysteriously",
		       "buggily", "extremely", "nicely", "strangely",
		       "irritatingly", "unquestionably", "clearly",
		       "plainly", "silently", "abstractly", "validly",
		       "invalidly", "immutably", "oddly", "disturbingly",
		       "atonally", "randomly", "amusingly", "widely",
		       "narrowly", "manually", "automatically", "audibly",
		       "brilliantly", "independently", "definitively",
		       "provably", "improbably", "distortingly",
		       "confusingly"]
adjs2 = ["invalid", "valid",
		       "referenced", "dereferenced", "unreferenced",
		       "illegal", "legal",
		       "questionable", 
		       "alternate", "implemented", "unimplemented",
		       "terminal", "non-terminal",
		       "static", "dynamic",
		       "qualified", "unqualified", 
		       "constant", "variable",
		       "volatile", "non-volatile",
		       "abstract", "concrete",
		       "fungible", "non-fungible",
		       "untyped", "variable",
		       "mutable", "immutable",
		       "sizable", "miniscule",
		       "perverse", "immovable",
		       "compressed", "uncompressed",
		       "surreal", "allegorical"]
nouns = ["pointer", "structure",
		       "definition", "declaration", "type", "union",
		       "coder", "admin", "hacker", "kitten", "mistake",
		       "conversion", "implementation", "design", "analysis",
		       "neophyte", "expert", "bundle", "package",
		       "abstraction", "theorem", "display", "distro",
		       "restriction", "device", "function", "reference"]
a1 = random.choice(adjs1)
a2 = random.choice(adjs2)
n1 = random.choice(nouns)
if a1[0] in ['a', 'e', 'i', 'o', 'u']:
    start = 'an'
else:
    start = 'a'
desc = '%s %s %s %s' % (start, a1, a2, n1)
</%python>
<p>
<label for="registration.silly_description">Description:</label>
<% desc %>
<% h.hidden_field('registration.silly_description', value=desc) %>
</p>

<p>
<label for="registration.prevlca">Have you attended any previous LCAs?</label>

% for (year, desc) in [('99', '1999 (CALU, Melbourne)'), ('01', '2001 (Sydney)'), ('02', '2002 (Brisbane)'), ('03', '2003 (Perth)'), ('04', '2004 (Adelaide)'), ('05', '2005 (Canberra)'), ('06', '2006 (Dunedin)')]:
%	label = 'registration.prevlca.%s' % year
<br />
<% h.check_box(label) %>
<label for="<% label %>"><% desc %></label>
% #endfor

</p>


</fieldset>

<fieldset id="registration">
<h4>Conference Information</h4>

<p>
<span class="mandatory">*</span> - Mandatory field
</p>

<p>
<span class="mandatory">*</span>
<label for="registration.type">What type of ticket do you want?</label>
<br />
# FIXME: dynamic content
% for (t, p, eb) in [('Professional', '690.00', '517.50'), ('Hobbyist', '300.00', '225.00'), ('Concession', '99.00', '99.00')]:
<input type="radio" name="registration.type" id="registration.type_<% t %>" value="<% t %>" />
<label for="registration.type_<% t %>"><% t %> - $<% p %> ($<% eb %> earlybird)</label>
<br />
% #endfor
<span class="fielddesc">
Check the <% h.link_to('registration page', url="/Registration", popup=True) %> for the full details of each ticket.
</span>
</p>

<p>
<label for="registration.discount_code">Discount Code:</label>
<% h.text_field('registration.discount_code') %>
</p>

<p>
<span class="mandatory">*</span>
<label>Teeshirt Size:</label>
<table>
# FIXME:
% for sex in ['M', 'F']:
<tr>
<td>
%	if sex == 'M':
Male:
%	else:
Female:
%	#endif
</td>
% 	for size, size_text in [('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'X Large'), ('XXL', 'XX Large'), ('XXXL', 'XXX Large')]:
<td>
<input type="radio" name="registration.teesize" id="registration.teesize_<% sex %>_<% size %>" value="<% sex %>_<% size %>" />
<label for="registration.teesize_<% sex %>_<% size %>"><% size_text %></label>
</td>
% 	#endfor
</tr>
% #endfor
</table>
</p>

<p>
<label for="registration.dinner">I'd like this many extra Penguin Dinner Tickets:</label>
<SELECT id="registration.dinner" name="registration.dinner">
<option value="0">0</option>
<option value="1">1</option>
<option value="2">2</option>
</SELECT> <label> - $60 each </label>
<br />
<span class="fielddesc">
The Penguin Dinner is included in the price of a Professional delegate ticket.  Concession and Hobbyist delegates will need to purchase a Penguin Dinner ticket if they wish to attend.
</span>
</p>

<p>
<label for="registration.diet">Dietary requirements:</label>
<br />
<% h.text_field('registration.diet', size=100) %>
</p>

<p>
<label for="registration.special">Other special requirements</label>
<br />
<% h.text_field('registration.special', size=100) %>
<br />
<span class="fielddesc">
Please enter any requirements if necessary; access requirements, etc.
</span>
</p>

<p>
<label for="registration.miniconfs">Prefered miniconfs:</label>

# FIXME: CLEARLY this needs to be dynamic

% for mc in ['Debian', 'Embedded', 'Education', 'FOSS in Research', 'FOSS in Movies', 'Gaming', 'GNOME', 'Kernel', 'Linuxchix', 'MySQL', 'OpenOffice.org', 'PostgreSQL', 'Virtualisation']:
% 	l = 'registration.miniconf.%s' % mc.replace(' ', '_')
<br />
<% h.check_box(l) %>
<label for="<% l %>"><% mc %></label>
% #endfor

<br />
<span class="fielddesc">
Please check the <% h.link_to('Miniconfs', url="/Miniconfs", popup=True) %> page for details on each event. You can choose to attend multiple miniconfs in the one day, as the schedules will be published ahead of the conference for you to swap sessions.
</span>
</p>

<p>
<label for="registration.opendaydrag">How many people are you bringing to <% h.link_to("Open Day", url="/OpenDay", popup=True) %>:</label>
<% h.text_field('registration.opendaydrag', size=10) %>
<br />
<span class="fielddesc">
Open Day is open to friends and family, and is targetted to a non-technical audience.  If you want to show off FOSS culture to some people, you can give us an idea of how many people to expect.
</span>
</p>

</fieldset>

<fieldset id="accommodation">
<h4>Accommodation</h4>

<p>
<span class="mandatory">*</span> - Mandatory field
</p>


<p>
Please check out the <% h.link_to('accommodation', url="/Accommodation", popup=True) %> page before committing to any accommodation choices.
</p>

<p>
<span class="mandatory">*</span>
<label for="registration.accommodation">What accommodation would you like to stay at:</label>
<SELECT name="registration.accommodation">
<option value="0">I will organise my own</option>
% for a in c.accommodation_collection:
<option value="<% a.id %>"><% a.name %>
% 	if a.option:
(<% a.option %>)
% 	#endif
- <% h.number_to_currency(a.cost_per_night) %> per night</option>
% #endfor
</SELECT>
</p>

<p>
<span class="mandatory">*</span>
<label for="registration.checkin">Check in on:</label>
<select name="registration.checkin">
% for d in range(14, 20):
<option value="<% d %>"><% datetime.datetime(2007, 1, d).strftime('%A, %d %b') %></option>
% #endfor
</select>
</p>

<p>
<span class="mandatory">*</span>
<label for="registation.checkout">Check out on:</label>
<select name="registration.checkout">
% for d in range(15, 21):
<option value="<% d %>"
% 	if d == 20:
selected
% 	#endif
><% datetime.datetime(2007, 1, d).strftime('%A, %d %b') %></option>
% #endfor
</select>
</p>
</fieldset>

<fieldset id="partners">
<h4>Partners Programme</h4>

<p>
<label for="registration.partner_email">Your partner's email address:</label>
<% h.text_field('registration.partner_email', size=50) %>
<br />
<span class="fielddesc">
If you are planning on bringing your partner, please enter their email address here so that our <% h.link_to('Partners Programme', url="/PartnersProgramme", popup=True) %> manager can contact them.  <% h.link_to("Contact us", url="/PartnersProgramme", popup=True) %> if you have any problems registering your partner for the programme.
</span>
</p>

<p>
<label for="registration.children">Are you bringing children?</label>
<br />
<label for="registration.kids_0_3">This many under 3 year olds:</label>
<% h.text_field('registration.kids_0_3', size=10) %>
<br />
<label for="registration.kids_4_6">This many 4-6 year olds:</label>
<% h.text_field('registration.kids_4_6', size=10) %>
<br />
<label for="registration.kids_7_9">This many 7-9 year olds:</label>
<% h.text_field('registration.kids_7_9', size=10) %>
<br />
<label for="registration.kids_10">This many aged 10 or above:</label>
<% h.text_field('registration.kids_10', size=10) %>
<br />
</p>
</fieldset>

<fieldset>
<h4>Subscriptions</h4>

<p>
<% h.check_box('registration.lasignup') %>
<label for="registration.lasignup">I want to sign up for (free) LA membership!</label>
</p>

<p>
<% h.check_box('registration.announcesignup') %>
<label for="registration.announcesignup">I want to sign up to the low traffic conference announcement mailing list!</label>
</p>

<p>
<% h.check_box('registration.delegatesignup') %>
<label for="registration.delegatesignup">I want to sign up to the conference attendees mailing list!</label>
</p>

</fieldset>

<% h.submit("Register me!") %>
<span class="fielddesc">
If you encounter any problems signing up please email <a href="mailto:seven-contact@lca2007.linux.org.au">seven-contact@lca2007.linux.org.au</a>
</span>


<% h.end_form() %>
</&>

<%args>
defaults
errors
</%args>

<%init>
import datetime
import random

# work around bug in formencode, set defaults
if not defaults:
	defaults = {'registration.checkout': '20',
		'registration.lasignup': '1',
		'registration.announcesignup': '1',
		'registration.dinner': '0',
		}
</%init>

