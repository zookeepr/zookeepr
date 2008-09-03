<fieldset id="personal">

<h2>Personal Information</h2>

<br><p class="note">
<span class="mandatory">*</span> - Mandatory field
</p>

<p class="label">
<span class="mandatory">*</span>
<label for="person.address">Address:</label>
</p><p class="entries">
<% h.textfield('person.address1', size=40) %>
<br>
<% h.textfield('person.address2', size=40) %>
</p>
<p class="label">
<span class="mandatory">*</span>
<label for="person.city">City/Suburb:</label>
</p><p class="entries">
<% h.textfield('person.city', size=40) %>
</p><p class="label">
<label for="person.state">State/Province:</label>
</p><p class="entries">
<% h.textfield('person.state', size=40) %>
</p><p class="label">
<span class="mandatory">*</span>
<label for="person.country">Country:</label>
</p><p class="entries">
<select name="person.country">
% for country in h.countries():
<option value="<%country%>"><% country %></option>
% #endfor
</select>
</p><p class="label">
<span class="mandatory">*</span>
<label for="person.postcode">Postcode/ZIP:</label>
</p><p class="entries">
<% h.textfield('person.postcode', size=40) %>
</p>

% if 'signed_in_person_id' in session:
%   proposals = c.signed_in_person.proposals
%   is_speaker = reduce(lambda a, b: a or b.accepted, proposals, False)
% else:
%   proposals = []
%   is_speaker = False
% #endif

<p class="label"><label for="person.mobile">Phone number:</label>
</p><p class="entries">
<% h.textfield('person.phone') %>
</p>

<p class="label">
% if is_speaker:
<span class="mandatory">*</span>
% #endif
<label for="person.mobile">Mobile/Cell number:</label>
</p><p class="entries">
<% h.textfield('person.mobile') %>
</p>

</p><p class="label">
<label for="person.company">Company:</label>
</p><p class="entries">
<% h.textfield('person.company', size=60) %>
</p>

<p class="label">
<span class="mandatory">*</span>
<label for="registration.checkin">Check in on:</label>
</p><p class="entries">
<select name="registration.checkin">
% dates = [(d, 1) for d in range(18,26)]
% for (day, month) in dates:
<option value="<% day %>"><% datetime.datetime(2009, month, day).strftime('%A, %e %b') %></option>
% #endfor
</select>
</p>

<p class="label">
<span class="mandatory">*</span>
<label for="registation.checkout">Check out on:</label>
</p><p class="entries">
<select name="registration.checkout">
% for day, month in dates[1:]:
<option value="<% day %>" ><% datetime.datetime(2008, month, day).strftime('%A, %e %b') %></option>
% #endfor
</select>
</p>
</fieldset>

<fieldset id="partners">
<h2>Partners Programme</h2>

<p class="label">
<label for="registration.partner_email">Your partner's email address:</label>
</p><p class="entries">
<% h.textfield('registration.partner_email', size=50) %>
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
</p><p class="entries">
% if is_speaker:
%   price = '&#215; $0.00'
% else:
%   price = '&#215; $220.00'
% #endif
<label for="registration.pp_adults">Adults:</label>
<% h.textfield('registration.pp_adults', size=10) %>
<% price %>
<br>
<label for="registration.kids_12_17">Young adults (12-17):</label>
<% h.textfield('registration.kids_12_17', size=10) %>
<% price %>
<br>
% if is_speaker:
%   price = '&#215; $0.00'
% else:
%   price = '&#215; $132.00'
% #endif
<label for="registration.kids_10_11">Children 10-11:</label>
<% h.textfield('registration.kids_10_11', size=10) %>
<% price %>
<br>
<label for="registration.kids_7_9">Children 7-9:</label>
<% h.textfield('registration.kids_7_9', size=10) %>
<% price %>
<br>
<label for="registration.kids_4_6">Children 4-6:</label>
<% h.textfield('registration.kids_4_6', size=10) %>
<% price %>
<br>
<label for="registration.kids_0_3">Children under 3:</label>
<% h.textfield('registration.kids_0_3', size=10) %>
<% price %>
<br>
</p>

% if is_speaker:
<p class="label">
<label for="registration.children">How many of the above do you want to pay for?</label>
</p><p class="entries">
<label for="registration.speaker_pp_pay_adult">Adults and young adults:</label>
<% h.textfield('registration.speaker_pp_pay_adult', size=10) %>
&#215; $220.00
<br>
<label for="registration.speaker_pp_pay_child">Children:</label>
<% h.textfield('registration.speaker_pp_pay_child', size=10) %>
&#215; $132.00
</p><p class="note">
As a speaker, your partner and your children are entitled to attend the
partners programme for free.
</p>
% else:
<% h.hidden_field('registration.speaker_pp_pay_adult', value=0) %>
<% h.hidden_field('registration.speaker_pp_pay_child', value=0) %>
% #endif
</fieldset>

<fieldset>
<h2>Further Information</h2>
<p class="label">
<label for="registration.diet">Dietary requirements:</label>
</p><p class="entries">
<% h.textfield('registration.diet', size=100) %>
</p>

<p class="label">
<label for="registration.special">Other special requirements</label>
</p><p class="entries">
<% h.textfield('registration.special', size=100) %>
</p><p class="note">
Please enter any requirements if necessary; access requirements, etc.
</p>

<p class="label">
<label for="registration.miniconfs">Preferred mini-confs:</label>
</p><p class="entries">

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
% 	l = 'registration.miniconf.%s' % mc.replace(' ', '_')
<% h.check_box(l) %>
<label for="<% l %>"><% mc %></label>
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
</p><p class="entries">
<% h.textfield('registration.opendaydrag', size=10) %>
</p><p class="note">
<!-- <% h.link_to("Open Day", url="/programme/open-day", popup=True) %> -->
Open Day
<!-- -->
is open to friends and family, and is targeted to a non-technical
audience.  If you want to show off FOSS culture to some people, you can
give us an idea of how many people to expect.
</p>

<p class="label">
# FIXME: dynamic :)
<label for="registration.shell">Your favourite shell:</label>
</p><p class="entries">
<select id="registration.shell" name="registration.shell" onchange="toggle_select_hidden(this.id, 'shell_other')">
<option value="-">(please select)</option>
% for s in ['bash', 'sh', 'csh', 'tcsh', 'emacs', 'ksh', 'smrsh', 'busybox', 'dash', 'XTree Gold', 'zsh']:
<option value="<%s%>"><% s %></option>
% #endfor
<option value="other">OTHER:</option>
</SELECT>
<span id="shell_other"><% h.textfield('registration.shelltext') %></span>
</p>

<p class="label">
<label for="registration.editor">Your favourite editor:</label>
</p><p class="entries">
<select id="registration.editor" name="registration.editor" onchange="toggle_select_hidden(this.id, 'editor_other')">
<option value="-">(please select)</option>
% for e in ['vi', 'vim', 'emacs', 'xemacs', 'gedit', 'nano', 'kate', 'jed', 'bluefish']:
<option value="<% e %>"><% e %></option>
% #endfor
<option value="other">OTHER:</option>
</SELECT>
<span id="editor_other"><% h.textfield('registration.shelltext') %></span>
</p>

<p class="label">
<label for="registration.distro">Your favourite distro:</label>
</p><p class="entries">
<select id="registration.distro" name="registration.distro" onchange="toggle_select_hidden(this.id, 'distro_other')">
<option value="-">(please select)</option>
% for d in ['CentOS', 'Darwin', 'Debian', 'Fedora', 'FreeBSD', 'Gentoo', 'L4', 'Mandriva', 'NetBSD', 'Nexenta', 'OpenBSD', 'OpenSolaris', 'OpenSUSE', 'Oracle Enterprise Linux', 'RHEL', 'Slackware', 'Ubuntu']:
<option value="<% d %>"><% d %></option>
% #endfor
<option value="other">OTHER:</option>
</SELECT>
<span id="distro_other"><% h.textfield('registration.shelltext') %></span>
</p>

</p><p class="label">
<label for="registration.nick">Superhero name:</label>
</p><p class="entries">
<% h.textfield('registration.nick', size=30) %>
</p><p class="note">
Your IRC nick or other handle you go by.
</p>

<p class="label">
<label for="registration.prevlca">Have you attended linux.conf.au before?</label>
</p><p class="entries">
% for (year, desc) in [('99', '1999 (CALU, Melbourne)'), ('01', '2001 (Sydney)'), ('02', '2002 (Brisbane)'), ('03', '2003 (Perth)'), ('04', '2004 (Adelaide)'), ('05', '2005 (Canberra)'), ('06', '2006 (Dunedin)'), ('07', '2007 (Sydney)'), ('08', '2008 (Melbourne)')]:
%   label = 'registration.prevlca.%s' % year
<br>
<% h.check_box(label) %>
<label for="<% label %>"><% desc %></label>
% #endfor
</p>


<%python>
starts = ["a", "a", "a", "one", "no"] # bias toward "a"
adverbs = ["strongly",
		       "poorly", "badly", "well", "dynamically",
		       "hastily", "statically", "mysteriously",
		       "buggily", "extremely", "nicely", "strangely",
		       "irritatingly", "unquestionably", "clearly",
		       "plainly", "silently", "abstractly", "validly",
		       "invalidly", "immutably", "oddly", "disturbingly",
		       "atonally", "randomly", "amusingly", "widely",
		       "narrowly", "manually", "automatically", "audibly",
		       "brilliantly", "independently", "definitively",
		       "provably", "improbably", "distortingly",
		       "confusingly", "decidedly", "historically"]
adjectives = ["invalid", "valid",
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
		       "surreal", "allegorical",
		       "trivial", "nontrivial"]
nouns = ["pointer", "structure",
		       "definition", "declaration", "type", "union",
		       "coder", "admin", "hacker", "kitten", "mistake",
		       "conversion", "implementation", "design", "analysis",
		       "neophyte", "expert", "bundle", "package",
		       "abstraction", "theorem", "display", "distro",
		       "restriction", "device", "function", "reference"]
adverb = random.choice(adverbs)
adjective = random.choice(adjectives)
noun = random.choice(nouns)
start = random.choice(starts)
if start == 'a' and adverb[0] in ['a', 'e', 'i', 'o', 'u']:
    start = 'an'
desc = '%s %s %s %s' % (start, adverb, adjective, noun)
descMD5 = md5.new(desc).hexdigest()
</%python>
<p class="label">
<label for="registration.silly_description">Description:</label>
</p>
<blockquote><p>
<% desc %>
<% h.hidden_field('registration.silly_description', value=desc) %>
</p></blockquote>
<p class="note">
This is a randomly chosen description for your name badge
</p>

</fieldset>

<fieldset>
<h2>Subscriptions</h2>

<p class="entries">
<% h.check_box('registration.lasignup') %>
<label for="registration.lasignup">I want to sign up for (free) Linux Australia membership!</label>
</p>

<p class="entries">
<% h.check_box('registration.announcesignup') %>
<label for="registration.announcesignup">I want to sign up to the low traffic conference announcement mailing list!</label>
</p>

<p class="entries">
<% h.check_box('registration.delegatesignup') %>
<label for="registration.delegatesignup">I want to sign up to the conference attendees mailing list!</label>
</p>

</fieldset>

% if is_speaker:
<fieldset>
<h2>Speaker recording consent and release</h2>
<p>As a service to Linux Australia members and to other interested Linux users,
Linux Australia would like to make your presentation available to the public.
This involves video­taping your talk, and offering the video/audio and slides
(for download, or on CD­ROM).</p>

<p class="entries">
<% h.check_box('registration.speaker_record') %>
<label for="registration.speaker_record">I allow Linux Australia to record my presentation</label>
</p>

<p class="entries">
<% h.check_box('registration.speaker_video_release') %>
<label for="registration.speaker_video_release">I allow Linux Australia to
release my video under the Creative Commons ShareAlike License</label>
</p>

<p class="entries">
<% h.check_box('registration.speaker_slides_release') %>
<label for="registration.speaker_slides_release">I allow Linux Australia to share my slides</label>
</p>

<p>If you have allowed Linux Australia to publish your slides, there will
be an upload mechanism closer to the conference. We will publish them under
the Creative Commons Attribution License unless you have an equivalent
preference that you let us know.</p>

</fieldset>
% #endif

<br>
<% h.hidden_field('registration.silly_description_md5', value=descMD5) %>
<%init>
import datetime
import md5
import random
</%init>
