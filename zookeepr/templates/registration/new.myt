<h3>Register for the conference</h3>

<p>
Welcome to the conference registration. Please fill in the form as best you can. 
</p>

<p>
If you've already got an account, but can't log in, you can
<% h.link_to('recover your password', url=h.url(controller='account', action='forgotten_password', id=None)) %>.
</p>

<&| @zookeepr.lib.form:fill, defaults=defaults, errors=errors &>
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

<fieldset id="registration">
<h4>Conference Information</h4>

<p>
<label for="registration.special">Special requirements</label>
<br />
<% h.text_field('registration.special', size=100) %>
<br />
<span class="fielddesc">
Please enter any requirements; dietary, access requirements, or otherwise.
</span>
</p>

<p>
<span class="mandatory">*</span>
I'd like to choose the 
<% h.select('registration.type', option_tags=h.options_for_select_from_objects(c.registration, 'name', 'id')) %>
<label for="registration.type">registration</label>.
Check the <% h.link_to('registration page', url="Registration") %> for full details on each ticket.
</p>

<p>
<span class="mandatory">*</span>
<label for="registration.miniconfs">Prefered miniconfs:</label>
<br />
#<% h.check_box('registration.miniconfs', option_tags=h.options_for_select_from_objects(c.registration, 'name', 'id')) %>
<span class="fielddesc">
Please check the <a href="http://lca2007.linux.org.au/Miniconfs">Miniconfs</a> page for details on each event. You can choose to attend multiple miniconfs in the one day, as the schedules will be published ahead of the conference for you to swap sessions.
</span>

<h5>Monday</h5>
<INPUT type="checkbox">Embedded Miniconf
<br />
<INPUT type="checkbox">Virtualisation Miniconf
<br />
<INPUT type="checkbox">MySQL Miniconf
<br />
<INPUT type="checkbox">FOSS in Research Miniconf
<br />
<INPUT type="checkbox">FOSS in the Movies Miniconf
<h5>Tuesday</h5>
<br />
<INPUT type="checkbox">Gaming Miniconf
<br />
<INPUT type="checkbox">Kernel Miniconf
<br />
<INPUT type="checkbox">PostgreSQL Miniconf
<br />
<INPUT type="checkbox">OpenOffice.org Miniconf
<br />
<INPUT type="checkbox">Linuxchix Miniconf
<h5>Both Monday and Tuesday</h5>

<INPUT type="checkbox">Debian Miniconf
<br />
<INPUT type="checkbox">GNOME
<br />
<INPUT type="checkbox">Education
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
<span class="mandatory">*</span>
<label for="registration.type">T-shirt Size:</label>
<SELECT>
<option>S</option>
<option>M</option>
<option>L</option>
<option>XL</option>
<option>XXL</option>
<option>XXXL</option>
</SELECT>
</p>

<p>
<label for="registration.opendaydrag">I'm dragging this many people along to <% h.link_to("Open Day", url="OpenDay") %>:</label>
<INPUT type="text">
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
<label for="registration.shell">My favourite shell:</label>
<SELECT>
<option>Bash</option>
<option>Zsh</option>
<option>Ksh</option>
</SELECT>
Other: <INPUT type="text">
</p>

<p>
<label for="registration.editor">Your favourite editor:</label>
<SELECT>
<option>Vim</option>
<option>Emacs</option>
<option>Gedit</option>
</SELECT>
Other: <INPUT type="text">
</p>

<p>
<label for="registration.distro">Your favourite distro:</label>
<SELECT>
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

<p>
<label for="registration.keysigning">I'll be attending the keysigning?</label>
<INPUT type="checkbox">
</p>
</fieldset>

<fieldset id="partners">
<h4>Partners Programme</h4>

<p>
<label for="registration.partners">I'll be bringing a partner?</label>
<INPUT type="checkbox">
</p>
<p>
<label for="registration.partneremail">My partner's email address</label> (so our <a href="http://lca2007.linux.org.au/PartnersProgramme">Partners Programme</a> tsar can contact them!)<br />
<INPUT type="text">
</p>

<p>
<label for="registration.children">I'll be bringing children?</label>
<br />
<label for="registration.kids0-5">This many 0-3 year olds:</label><INPUT type="text"><br />
<label for="registration.kids0-5">This many 4-6 year olds:</label><INPUT type="text"><br />
<label for="registration.kids0-5">This many 7-9 year olds:</label><INPUT type="text"><br />
<label for="registration.kids0-5">This many 10 or above:</label><INPUT type="text"><br />
</p>
</fieldset>

<fieldset id="accommodation">
<h4>Accommodation</h4>

<p>
Please check out the <a href="http://lca2007.linux.org.au/Accommodation">accommodation</a> page before committing to any accommodation choices.
</p>

<p>
<span class="mandatory">*</span>
<label for="registration.accommodation">I would like the following accommodation:</label>
<SELECT>
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
<label for="registration.accommodationdays">I'd like accommodation on the following days:</label>
<br />
<INPUT type="checkbox">Sunday
<INPUT type="checkbox">Monday
<INPUT type="checkbox">Tuesday
<INPUT type="checkbox">Wednesday
<INPUT type="checkbox">Thursday
<INPUT type="checkbox">Friday
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
<label for="registration.discount">Discount codes</label> - enter the special discount code if you have one.<br />
<INPUT type="text">
</p>


<p>
<span class="mandatory">*</span> - Mandatory field
</p>

</fieldset>

<% h.submit("Register me!") %>

<% h.end_form() %>
</&>

<%args>
defaults
errors
</%args>
