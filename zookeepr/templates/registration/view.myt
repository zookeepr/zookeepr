<h2>Your registration details</h2>

<p>Here are the registration details we have for you.</p>

<p><a href="/registration/status">Registration status</a></p>

<h2>About yourself</h2>

<p class="label">
<label for="person.firstname">Your first name:</label></p>
<p>
<% c.registration.person.firstname | h %>
</p>

<p class="label">
<label for="person.lastname">Your last name:</label></p>
<p>
<% c.registration.person.lastname | h %>

<p class="label">
<label for="person.email_address">Email address:</label></p>
<p>
<% c.registration.person.email_address | h %>
</p>
<p class="note">
Your email address will only be used to correspond with you, and is your login name for the website.  It will not be shown or used otherwise.
</p>

<h2>Personal Information</h2>

<p class="label">
<span class="mandatory">*</span>
<label for="registration.address">Address:</label>
</p><p >
<% c.registration.address1 %>
<br />
<% c.registration.address2 %>
</p>
<p class="label">
<span class="mandatory">*</span>
<label for="registration.city">City/Suburb:</label>
</p><p >
<% c.registration.city %>
</p><p class="label">
<label for="registration.state">State/Province:</label>
</p><p >
<% c.registration.state %>
</p><p class="label">
<span class="mandatory">*</span>
<label for="registration.country">Country:</label>
</p><p >
<% c.registration.country %>
</p><p class="label">
<span class="mandatory">*</span>
<label for="registration.postcode">Postcode/ZIP:</label>
</p><p >
<% c.registration.postcode %>
</p>

% if 'signed_in_person_id' in session:
%   proposals = c.signed_in_person.proposals
%   is_speaker = reduce(lambda a, b: a or b.accepted, proposals, False)
% else:
%   proposals = []
%   is_speaker = False
% #endif

<p class="label">
% if is_speaker:
<span class="mandatory">*</span>
% #endif
Mobile/Cell number:
</p><p >
<% c.registration.person.mobile %>
</p>

</p><p class="label">
<label for="registration.company">Company:</label>
</p><p >
<% c.registration.company %>
</p>

<p class="label">
# FIXME: dynamic :)
<label for="registration.shell">Your favourite shell:</label>
</p><p >
<% c.registration.shelltext or c.registration.shell %>
</p>


<p class="label">
<label for="registration.editor">Your favourite editor:</label>
</p><p >
<% c.registration.editortext or c.registration.editor %>
</p>

<p class="label">
<label for="registration.distro">Your favourite distro:</label>
</p><p >
<% c.registration.distrotext or c.registration.distro %>
</p>

</p><p class="label">
<label for="registration.nick">Superhero name:</label>
</p><p >
<% c.registration.nick %>
</p><p class="note">
Your IRC nick or other handle you go by.
</p>

<p class="label">
<label for="registration.silly_description">Description:</label>
</p><p>
<% c.registration.silly_description %>
</p>

<p class="label">
<label for="registration.prevlca">Have you attended linux.conf.au before?</label>
</p><p >
% for (year, desc) in [('99', '1999 (CALU, Melbourne)'), ('01', '2001 (Sydney)'), ('02', '2002 (Brisbane)'), ('03', '2003 (Perth)'), ('04', '2004 (Adelaide)'), ('05', '2005 (Canberra)'), ('06', '2006 (Dunedin)'), ('07', '2007 (Sydney)')]:
%	label = 'registration.prevlca.%s' % year
<br />
<% yesno(year in (c.registration.prevlca or [])) %>
<% desc %>
% #endfor
</p>

<h2>Conference Information</h2>

<p class="label">
<label for="registration.type">Type of ticket:</label>
</p><p >
<% c.registration.type %>
</p>
<p class="note">
Check the <% h.link_to('registration page', url="/register") %> for the
full details of each ticket.  One important change from past years is that
Student and Hobbyist tickets also include Penguin Dinner.
</p>

% if 0:
<p class="label">
<label for="registration.voucher_code">Voucher Code:</label>
</p><p >
<% c.registration.voucher_code %>
</p>
% else:
<% h.hidden_field('registration.voucher_code', value='') %>
% #endif

<p class="label">
<label>T-shirt Size and Style:</label>
<p >
<%python>
teesize = c.registration.teesize.split('_')

try:
  teesize[0] = {
    'M': 'Mens',
    'F': 'Womens',
  }.get(teesize[0], teesize[0])

  teesize[1] = {
    'long': 'long-sleeve',
    'short': 'short-sleeve',
  }.get(teesize[1], teesize[1])
except:
  pass

teesize = ' '.join(teesize)

</%python>
<% teesize %>
</p><p class="note">
A conference T-shirt is included with your ticket.
</p>

<p class="label">Additional T-shirts:</label>
</p><p >
<% c.registration.extra_tee_count or 0 %>
&#215; $24.75 each; sizes and styles:
<% c.registration.extra_tee_sizes |h%>
</p>


<p class="label">
<label for="registration.dinner">Additional Penguin Dinner Tickets:</label>
</p><p >
<% c.registration.dinner %>
&#215; $50 each; not counting yourself.
</p><p class="note">
One Penguin Dinner is included in the
price of your conference ticket.  Additional Penguin Dinner tickets are
intended for partners or friends not
attending the conference.
</p><p class="note-bene">
Note that unlike past years, <b>Student and Hobbyist tickets already
include</b> one Penguin Dinner ticket.
</p>

<p class="label">
<label for="registration.diet">Dietary requirements:</label>
</p><p >
<% c.registration.diet or "(none entered)" %>
</p>

<p class="label">
<label for="registration.special">Other special requirements</label>
</p><p >
<% c.registration.special or "(none entered)" %>
</p>

<p class="label">
<label for="registration.miniconfs">Preferred mini-confs:</label>
</p><p >

<%python>
# FIXME: CLEARLY this needs to be dynamic
mclist = (
    ('Monday',
	('Debian', 'Education', 'Embedded', 'Fedora', 'Multimedia', 'Security',
	'Virtualisation', 'Wireless')),
    ('Tuesday',
	('Distro Summit', 'Gaming', 'Gentoo', 'GNOME.conf.au', 'Kernel',
	'LinuxChix', 'MySQL', 'SysAdmin')))
</%python>
<table><tr>
% for day, mcs in mclist: 
<th><% day %>
% #endfor
<tr>
% for day, mcs in mclist: 
<td>
%   for mc in mcs:
%       l = {'GNOME.conf.au': 'GNOME'}.get(mc, mc).replace(' ', '_')
<% yesno(l in (c.registration.miniconf or [])) %>
<% mc %>
<br>
%   #endfor
&nbsp;
% #endfor
</table>

<p class="note">
Please check the <% h.link_to('mini-confs', url="/programme/mini-confs") %>
page for details on each event. You can choose to attend multiple mini-confs in the one day, as the schedules will be published ahead of the conference for you to swap sessions.
</p>

<p class="label">
<label for="registration.opendaydrag">How many people are you bringing to Open Day?</label>
</p><p >
<% num(c.registration.opendaydrag) %>
</p><p class="note">
<!-- <% h.link_to("Open Day", url="/programme/open-day", popup=True) %> -->
Open Day
<!-- -->
is open to friends and family, and is targeted to a non-technical
audience.  If you want to show off FOSS culture to some people, you can
give us an idea of how many people to expect.
</p>

</fieldset>

<fieldset id="accommodation">
<h2>Accommodation</h2>

<p>
Please check the <% h.link_to('accommodation', url="/register/accommodation") %>
page for more details.
</p>

% if c.registration.accommodation:
<p class="label">
Accommodation type
</p><p>
<% c.registration.accommodation.name %>
%   if c.registration.accommodation.option:
(<% c.registration.accommodation.option %>)
%   #endif
- $<% "%.2f" % c.registration.accommodation.cost_per_night %> per night
</p>

<p class="label">
<label for="registration.checkin">Check in on:</label>
</p><p >
<% date(c.registration.checkin) %>
</p>

<p class="label">
<span class="mandatory">*</span>
<label for="registation.checkout">Check out on:</label>
</p><p >
<% date(c.registration.checkout) %>
</p>
% else:
<p>
I will organise my own.
</p>
% #endif

<fieldset id="partners">
<h2>Partners Programme</h2>

<p class="label">
<label for="registration.partner_email">Your partner's email address:</label>
</p><p >
<% c.registration.partner_email or "(none given)" %>
</p><p class="note">
If you are planning on bringing your partner, please enter their email
address here so that our
<!--
<% h.link_to('Partners Programme', url="/PartnersProgramme", popup=True) %>
-->
Partners Programme
<!-- -->
manager can contact them.
</p>

<p class="label">
<label for="registration.children">How many people for the partners
programme?</label>
</p><p >
% if is_speaker:
%   price = '&#215; $0.00'
% else:
%   price = '&#215; $297.00'
% #endif
<label for="registration.pp_adults">Adults:</label>
<% num(c.registration.pp_adults) %>
<% price %>
<br />
<label for="registration.kids_12_17">Young adults (12-17):</label>
<% num(c.registration.kids_12_17) %>
<% price %>
<br />
% if is_speaker:
%   price = '&#215; $0.00'
% else:
%   price = '&#215; $143.00'
% #endif
<label for="registration.kids_10_11">Children 10-11:</label>
<% num(c.registration.kids_10_11) %>
<% price %>
<br />
<label for="registration.kids_7_9">Children 7-9:</label>
<% num(c.registration.kids_7_9) %>
<% price %>
<br />
<label for="registration.kids_4_6">Children 4-6:</label>
<% num(c.registration.kids_4_6) %>
<% price %>
<br />
<label for="registration.kids_0_3">Children under 3:</label>
<% num(c.registration.kids_0_3) %>
<% price %>
<br />
</p>

% if is_speaker:
<p class="label">
<label for="registration.children">How many of the above do you want to pay for?</label>
</p><p >
<label for="registration.speaker_pp_pay_adult">Adults and young adults:</label>
<% num(c.registration.speaker_pp_pay_adult) %>
&#215; $297.00
<br />
<label for="registration.speaker_pp_pay_child">Children:</label>
<% num(c.registration.speaker_pp_pay_child) %>
&#215; $143.00
</p><p class="note">
As a speaker, your partner and your children are entitled to attend the
partners programme for free.
</p>
% else:
%    pass
% #endif

<h2>Subscriptions</h2>

<p >
<% yesno(c.registration.lasignup) %>
<label for="registration.lasignup">I want to sign up for (free) Linux Australia membership!</label>
</p>

<p >
<% yesno(c.registration.announcesignup) %>
<label for="registration.announcesignup">I want to sign up to the low traffic conference announcement mailing list!</label>
</p>

<p >
<% yesno(c.registration.delegatesignup) %>
<label for="registration.delegatesignup">I want to sign up to the conference attendees mailing list!</label>
</p>

</fieldset>

% if is_speaker:
<h2>Speaker recording consent and release</h2>
<p>As a service to Linux Australia members and to other interested Linux users,
Linux Australia would like to make your presentation available to the public.
This involves video­taping your talk, and offering the video/audio and slides
(for download, or on CD­ROM).</p>

<p >
<% yesno(c.registration.speaker_record) %>
<label for="registration.speaker_record">I allow Linux Australia to record my presentation</label>
</p>

<p >
<% yesno(c.registration.speaker_video_release) %>
<label for="registration.speaker_video_release">I allow Linux Australia to
release my video under the Creative Commons ShareAlike License</label>
</p>

<p >
<% yesno(c.registration.speaker_slides_release) %>
<label for="registration.speaker_slides_release">I allow Linux Australia to share my slides</label>
</p>

<p>If you have allowed Linux Australia to publish your slides, there will
be an upload mechanism closer to the conference. We will publish them under
the Creative Commons Attribution License unless you have an equivalent
preference that you let us know.</p>
% #endif

<p><br/><a href="/registration/status">Registration status</a></p>

<%init>
def yesno(bool):
    if bool:
        return '&#9745'
    else:
        return '&#9744'
def num(x):
    if x==None:
        return 'none'
    else:
        return x
def date(d):
    if d==1:
        return "%dst of February" % d
    elif d==2:
        return "%dnd of February" % d
    elif d==3:
        return "%drd of February" % d
    elif d<15:
        return "%dth of February" % d
    elif d==31:
        return "%dst of January" % d
    else:
        return "%dth of January" % d

</%init>
