<%init>
import datetime
</%init>

<h3>Register for the conference</h3>

<p>
Welcome to the conference registration. Please fill in the form as best you can. 
</p>

<p>
If you've already got an account (through a prior registration, or other interaction with this site), but can't log in, you can try
<% h.link_to('recovering your password', url=h.url(controller='account', action='forgotten_password', id=None)) %>.
</p>

#<&| @zookeepr.lib.form:fill, defaults=defaults, errors=errors &>
<% h.form(h.url()) %>

<fieldset id="person">
<p>
<span class="mandatory">*</span>
<label for="person.fullname">Your full name:</label>
<br />
<% h.text_field('person.fullname', size=40) %>
</p>

<p>
<span class="mandatory">*</span>
<label for="person.email_address">Email address:</label>
<br />
<% h.text_field('person.email_address', size=40) %>
<br />
<span class="fielddesc">
Your email address will only be used to correspond with you, and is your login name for the website.  It will not be shown or used otherwise.
</span>
</p>

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

<p>
<span class="mandatory">*</span>
<label for="person.handle">Display name/handle/nickname:</label>
<br />
<% h.text_field('person.handle', size=40) %>
<br />
<span class="fielddesc">
Your display name will be used to identify you on the website.
</span>
</p>
</fieldset>

<fieldset id="personal">

<h4>Personal Information</h4>

<p>
<span class="mandatory">*</span>
<label for="registration.address">Address:</label>
<br />
<% h.text_field('registration.address1', size=40) %>
<br />
<% h.text_field('registration.address2', size=40) %>
<br />
<span class="mandatory">*</span>
<label for="registration.city">Suburb:</label>
<br />
<% h.text_field('registration.city', size=40) %>
<br />
<span class="mandatory">*</span>
<label for="registration.state">State:</label>
<br />
<% h.text_field('registration.state', size=40) %>
<br />
<span class="mandatory">*</span>
<label for="registration.country">Country:</label>
<br />
<% h.text_field('registration.country', size=40) %>
<br />
<span class="mandatory">*</span>
<label for="registration.postcode">Postcode:</label>
<br />
<% h.text_field('registration.postcode', size=40) %>
</p>

<p>
<label for="registration.shell">Your favourite shell:</label>
<SELECT>
<option>-</option>
<option>bash</option>
<option>zsh</option>
<option>ksh</option>
</SELECT>
Other: <INPUT type="text">
</p>

<p>
<label for="registration.editor">Your favourite editor:</label>
<SELECT>
<option>-</option>
<option>vim</option>
<option>emacs</option>
<option>gedit</option>
</SELECT>
Other: <INPUT type="text">
</p>

<p>
<label for="registration.distro">Your favourite distro:</label>
<SELECT>
<option>-</option>
<option>Ubuntu</option>
<option>Debian</option>
<option>Fedora</option>
<option>Mandriva</option>
<option>Gentoo</option>
<option>RHEL</option>
<option>CentOS</option>
<option></option>
</SELECT>
Other: <INPUT type="text">
</p>

<p>
<label for="registration.prevlca">Have you attended any previous LCAs?</label>

% for (year, desc) in [('99', '1999 (CALU, Melbourne)'), ('01', '2001 (Sydney)'), ('02', '2002 (Brisbane)'), ('03', '2003 (Perth)'), ('04', '2004 (Adelaide)'), ('05', '2005 (Canberra)'), ('06', '2006 (Dunedin)')]:
%	label = 'registration.prevlca%s' % year
<br />
<% h.check_box(label) %>
<label for="<% label %>"><% desc %></label>
% #endfor

</p>


</fieldset>

<fieldset id="partners">
<h4>Partners Programme</h4>

<p>
<label for="registration.partneremail">Your partner's email address:</label>
<% h.text_field('registration.partneremail', size=50) %>
<br />
<span class="fielddesc">
If you are planning on bringing your partner, please enter their email address here so that our <a href="http://lca2007.linux.org.au/PartnersProgramme">Partners Programme</a> manager can contact them.
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

<fieldset id="registration">
<h4>Conference Information</h4>

<p>
<span class="mandatory">*</span>
<label for="registration.type">What type of ticket do you want?</label>
<br />
% for t in ['Professional', 'Hobbyist', 'Student']:
<input type="radio" name="registration.type" id="registration.type_<% t %>" value="<% t %>" />
<label for="registration.type_<% t %>"><% t %></label>
<br />
% #endfor
<span class="fielddesc">
Check the <% h.link_to('registration page', url="/Registration") %> for full details on each ticket.
</span>
</p>

<p>
<label for="registration.discount">Discount Code:</label>
<% h.text_field('registration.discount') %>
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
<span class="mandatory">*</span>
<label for="registration.dinner">I'd like this many Penguin Dinner Tickets:</label>
<SELECT id="registration.dinner" name="registration.dinner">
<option>0</option>
<option selected>1</option>
<option>2</option>
</SELECT>
<br />
<span class="fielddesc">
The Penguin Dinner will be the official close of linux.conf.au 2007 and we strongly encourage people to attend.
 Not only will you have a chance to see who wins the Rusty Wrench Award, but you'll have a chance to drink with your buddies before the next lca.
</span>
<br />
<label for="registration.dinnerpref">Dietary requirements:</label>
<br />
<% h.text_field('registration.dinnerpref', size=100) %>
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
% 	l = 'registration.mc_%s' % mc.replace(' ', '_')
<br />
<% h.check_box(l) %>
<label for="<% l %>"><% mc %></label>
% #endfor

<br />
<span class="fielddesc">
Please check the <a href="http://lca2007.linux.org.au/Miniconfs">Miniconfs</a> page for details on each event. You can choose to attend multiple miniconfs in the one day, as the schedules will be published ahead of the conference for you to swap sessions.
</span>
</p>

<p>
<label for="registration.opendaydrag">How many people are you bringing to <% h.link_to("Open Day", url="/OpenDay") %>:</label>
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
Please check out the <a href="http://lca2007.linux.org.au/Accommodation">accommodation</a> page before committing to any accommodation choices.
</p>

<p>
<span class="mandatory">*</span>
<label for="registration.accommodation">Please pick the college would you like to stay at:</label>
<SELECT name="registration.accommodation">
<option>I will organise my own</option>
<option>New College - no breakfast $49.50</option>
<option>New College - $55.00</option>
<option>Shalom - $60.00</option>
<option>Shalom - with ensuite $80.00</option>
<option>International House - no breakfast $35.00</option>
<option>Warrane - male only $58.50</option>
</SELECT>
</p>

<p>
<span class="mandatory">*</span>
<label for="registration.accommodation_start">Check in on:</label>
<select name="registration.accommodation_start">
% for d in range(14, 21):
<option><% datetime.datetime(2007, 01, d).strftime('%A, %d %b') %></option>
% #endfor
</select>
</p>

<p>
<span class="mandatory">*</span>
<label for="registation.accommodation_end">Check out on:</label>
<select name="registration.accommodation_end">
% for d in range(14, 21):
<option 
% 	if d == 20:
selected
% 	#endif
><% datetime.datetime(2007, 01, d).strftime('%A, %d %b') %></option>
% #endfor
</select>
</p>
</fieldset>

<fieldset>
<h4>Subscriptions</h4>

<p>
<label for="registration.lasignup">I want to sign up for (free) LA membership!</label>
<INPUT type="checkbox" checked>
</p>

<p>
<label for="registration.announcesignup">I want to sign up to the low traffic conference announcement mailing list!</label>
<INPUT type="checkbox" checked>
</p>

<p>
<label for="registration.delegatessignup">I want to sign up to the conference attendees mailing list!</label>
<INPUT type="checkbox">
</p>

<p>
<span class="mandatory">*</span> - Mandatory field
</p>

</fieldset>

<% h.submit("Register me!") %>

<% h.end_form() %>
#</&>

<%args>
defaults
errors
</%args>
