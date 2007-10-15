<fieldset id="personal">

<h2>Personal Information</h2>

<br><p class="note">
<span class="mandatory">*</span> - Mandatory field
</p>

<p class="label">
<span class="mandatory">*</span>
<label for="registration.address">Address:</label>
</p><p class="entries">
<% h.text_field('registration.address1', size=40) %>
<br />
<% h.text_field('registration.address2', size=40) %>
</p>
<p class="label">
<span class="mandatory">*</span>
<label for="registration.city">City/Suburb:</label>
</p><p class="entries">
<% h.text_field('registration.city', size=40) %>
</p><p class="label">
<label for="registration.state">State/Province:</label>
</p><p class="entries">
<% h.text_field('registration.state', size=40) %>
</p><p class="label">
<span class="mandatory">*</span>
<label for="registration.country">Country:</label>
</p><p class="entries">
<% h.text_field('registration.country', size=40) %>
</p><p class="label">
<span class="mandatory">*</span>
<label for="registration.postcode">Postcode/ZIP:</label>
</p><p class="entries">
<% h.text_field('registration.postcode', size=40) %>
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
<label for="registration.phone">Mobile/Cell number:</label>
</p><p class="entries">
<% h.text_field('registration.phone') %>
</p>

</p><p class="label">
<label for="registration.company">Company:</label>
</p><p class="entries">
<% h.text_field('registration.company', size=60) %>
</p>

<p class="label">
# FIXME: dynamic :)
<label for="registration.shell">Your favourite shell:</label>
</p><p class="entries">
<select name="registration.shell">
<option value="-">-</option>
% for s in ['zsh', 'bash', 'sh', 'csh', 'tcsh', 'emacs', 'ksh', 'smrsh', 'busybox', 'dash', 'XTree Gold']:
<option value="<%s%>"><% s %></option>
% #endfor
</SELECT>
Other: <% h.text_field('registration.shelltext') %>
</p>

<p class="label">
<label for="registration.editor">Your favourite editor:</label>
</p><p class="entries">
<SELECT name="registration.editor">
<option value="-">-</option>
% for e in ['vi', 'vim', 'emacs', 'xemacs', 'gedit', 'nano', 'kate', 'jed', 'bluefish']:
<option value="<% e %>"><% e %></option>
% #endfor
</SELECT>
Other: <% h.text_field('registration.editortext') %>
</p>

<p class="label">
<label for="registration.distro">Your favourite distro:</label>
</p><p class="entries">
<SELECT name="registration.distro">
<option value="-">-</option>
% for d in ['CentOS', 'Darwin', 'Debian', 'Fedora', 'FreeBSD', 'Gentoo', 'L4', 'Mandriva', 'NetBSD', 'Nexenta', 'OpenBSD', 'OpenSolaris', 'OpenSUSE', 'RHEL', 'Slackware', 'Ubuntu']:
<option value="<% d %>"><% d %></option>
% #endfor
</SELECT>
Other: <% h.text_field('registration.distrotext') %>
</p>

</p><p class="label">
<label for="registration.nick">Superhero name:</label>
</p><p class="entries">
<% h.text_field('registration.nick', size=30) %>
</p><p class="note">
Your IRC nick or other handle you go by.
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
</p><p>
<% desc %>
<% h.hidden_field('registration.silly_description', value=desc) %>
</p>

<p class="label">
<label for="registration.prevlca">Have you attended linux.conf.au before?</label>
</p><p class="entries">
% for (year, desc) in [('99', '1999 (CALU, Melbourne)'), ('01', '2001 (Sydney)'), ('02', '2002 (Brisbane)'), ('03', '2003 (Perth)'), ('04', '2004 (Adelaide)'), ('05', '2005 (Canberra)'), ('06', '2006 (Dunedin)'), ('07', '2007 (Sydney)')]:
%	label = 'registration.prevlca.%s' % year
<br />
<% h.check_box(label) %>
<label for="<% label %>"><% desc %></label>
% #endfor
</p>


</fieldset>

<fieldset id="registration">
<h2>Conference Information</h2>

<br><p class="note">
<span class="mandatory">*</span> - Mandatory field
</p>

<p class="label">
<span class="mandatory">*</span>
<label for="registration.type">What type of ticket do you want?</label>
</p><p class="entries">
# FIXME: dynamic content
% ticket_types = [('Professional', '748.00', '598.40'), ('Hobbyist', '352.00', '281.60'), ('Concession', '154.00', '154.00')]
% if is_speaker:
%   ticket_types = [('Speaker', '0.00', '0.00')] + ticket_types
% #endif
% for (t, p, eb) in ticket_types:
<input type="radio" name="registration.type" id="registration.type_<% t %>" value="<% t %>" />
<label for="registration.type_<% t %>"><% t %> &#215; $<% p %>
% if eb != p:
($<% eb %> early-bird)
% #endif
</label>
<br />
% #endfor
% if is_speaker:
<p class="note-bene">
As a speaker, you are entitled to attend for free. However, if you
<i>want</i> to pay, we aren't stopping you :-)
</p>
% else:
<p class="note">
Check the <% h.link_to('registration page', url="/Registration", popup=True) %> for the full details of each ticket.
One important change from past years is that Concession and Hobbyist tickets
also include Penguin Dinner.
</p>
% #endif

% if 0:
<p class="label">
<label for="registration.discount_code">Discount Code:</label>
</p><p class="entries">
<% h.text_field('registration.discount_code') %>
</p>
% else:
<% h.hidden_field('registration.discount_code', value='') %>
% #endif

<p class="label">
<span class="mandatory">*</span>
<label>T-shirt Size and Style:</label>
<p class="entries">
<%python>
teeoptions = [
  ('F_long',
  """Women's long sleeve <br/><span class="note">(Small cut -
  order 1 size up)</p>""",
  ('8', '10', '12', '14', '16', '18', '', '')),

  ('F_short',
  "Women's short sleeve fitted",
  ('8', '10', '12', '14', '16', '', '', '')),

  ('M_long',
  "Men's long sleeve",
  ('S', 'M', 'L', 'XL', '2XL', '3XL', '', '')),

  ('M_short',
  "Men's short sleeve",
  ('S', 'M', 'L', 'XL', '2XL', '3XL', '4XL', '5XL'))]
teesizes = {}
def oddeven_gen():
  while 1:
    yield "odd"
    yield "even"
oddeven = oddeven_gen().next
</%python>
<table>
# FIXME:
% for style, style_text, sizes in teeoptions: 
<tr class="<% oddeven() %>">
<td>
<% style_text %> &nbsp;
</td>
% 	for size in sizes:
%           size_text = teesizes.get(size, size)
%           if size_text == '':
<td>&nbsp;</td>
%           else:
<td>
<input type="radio" name="registration.teesize" id="registration.teesize_<%
style %>_<% size %>" value="<% style %>_<% size %>" />&nbsp;<label for="registration.teesize_<% style %>_<% size %>"><% size_text %></label>&nbsp;
</td>
%           #endif
% 	#endfor
</tr>
% #endfor
</table>
</p><p class="note">
<br/>A conference T-shirt is included with your ticket. Please tell us
what size and shape you prefer.
</p>


<p class="label">
<label for="registration.dinner">Additional Penguin Dinner Tickets:</label>
</p><p class="entries">
<% h.text_field('registration.dinner', size=10) %>
&#215; $50 each; not counting yourself.
<p class="note">
One Penguin Dinner is included in the
price of your conference ticket.  Additional Penguin Dinner tickets are
intended for partners or friends not
attending the conference.
</p><p class="note-bene">
Note that unlike past years, <b>Concession and Hobbyist tickets already
include</b> one Penguin Dinner ticket.
</p>

<p class="label">
<label for="registration.diet">Dietary requirements:</label>
</p><p class="entries">
<% h.text_field('registration.diet', size=100) %>
</p>

<p class="label">
<label for="registration.special">Other special requirements</label>
</p><p class="entries">
<% h.text_field('registration.special', size=100) %>
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
<% h.text_field('registration.opendaydrag', size=10) %>
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

<br><p class="note">
<span class="mandatory">*</span> - Mandatory field
</p>


<p>
Please check out the <% h.link_to('accommodation', url="/register/accommodation", popup=True) %> page before committing to any accommodation choices.
</p>

<p class="label">
<span class="mandatory">*</span>
<label for="registration.accommodation">What accommodation would you like to stay at:</label>
</p><p class="entries">
<SELECT name="registration.accommodation">
<option value="0">I will organise my own</option>
% for a in c.accommodation_collection:
%    if a.beds==999:
%       places_left = ''
%    elif is_speaker and a.name=='Trinity':
%       places_left = ''
%    else:
%       places_left = '(%d places left)' % (a.beds - a.beds_taken)
%    #endif
%    if is_speaker or a.option!='speaker':
<option value="<% a.id %>"><% a.name %>
% 	if a.option:
(<% a.option %>)
% 	#endif
- <% h.number_to_currency(a.cost_per_night) %> per night <% places_left %></option>
%    #endif
% #endfor
</SELECT>
</p>

<p class="label">
<span class="mandatory">*</span>
<label for="registration.checkin">Check in on:</label>
</p><p class="entries">
<select name="registration.checkin">
% dates = [(d, 1) for d in range(27,32)] + [(d, 2) for d in (1,2,3)]
% for (day, month) in dates[:-1]:
<option value="<% day %>"><% datetime.datetime(2008, month, day).strftime('%A, %e %b') %></option>
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
<% h.text_field('registration.partner_email', size=50) %>
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
%   price = '&#215; $297.00'
% #endif
<label for="registration.pp_adults">Adults:</label>
<% h.text_field('registration.pp_adults', size=10) %>
<% price %>
<br />
<label for="registration.kids_12_17">Young adults (12-17):</label>
<% h.text_field('registration.kids_12_17', size=10) %>
<% price %>
<br />
% if is_speaker:
%   price = '&#215; $0.00'
% else:
%   price = '&#215; $143.00'
% #endif
<label for="registration.kids_10_11">Children 10-11:</label>
<% h.text_field('registration.kids_10_11', size=10) %>
<% price %>
<br />
<label for="registration.kids_7_9">Children 7-9:</label>
<% h.text_field('registration.kids_7_9', size=10) %>
<% price %>
<br />
<label for="registration.kids_4_6">Children 4-6:</label>
<% h.text_field('registration.kids_4_6', size=10) %>
<% price %>
<br />
<label for="registration.kids_0_3">Children under 3:</label>
<% h.text_field('registration.kids_0_3', size=10) %>
<% price %>
<br />
</p>

% if is_speaker:
<p class="label">
<label for="registration.children">How many of the above do you want to pay for?</label>
</p><p class="entries">
<label for="registration.speaker_pp_pay_adult">Adults and young adults:</label>
<% h.text_field('registration.speaker_pp_pay_adult', size=10) %>
&#215; $297.00
<br />
<label for="registration.speaker_pp_pay_child">Children:</label>
<% h.text_field('registration.speaker_pp_pay_child', size=10) %>
&#215; $143.00
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

<br/>
<% h.hidden_field('registration.silly_description_md5', value=descMD5) %>
<%init>
import datetime
import md5
import random
</%init>
