<%
# warning: this list must match the one in ../review/form.myt
miniconfs = (
  '(none)',
  'Debian',
  'Free as in Freedom',
  'Functional Programming',
  'Gaming',
  'Gentoo Down Under',
  'GNOME.conf.au',
  'High Performance Linix BoF',
  'Joomla!',
  'Lifehacker',
  'LinuxChix',
  'Linux Kernel',
  'Linux Security',
  'Mobile Devices',
  'Multimedia',
  'MythTV',
  'Open Source Databases',
  'Open Source Hardware',
  'Openoffice.org',
  'Perl',
  'Python',
  'Software Quality Assurance',
  'Systems Administration',
  'The Business of Open Source - for Software Developers',
  'Virtualization and Management',
)
%>

<%inherit file="/base.mako" />
<h2>Proposal Review - #${ c.proposal.id }</h2>

${ h.form(h.url_for()) }

% if not c.reviewed_everything:
<ul><li>${ h.link_to('Skip!', url=h.url_for(controller='proposal', action='review', id=c.next_review_id)) }</li></ul>
% else:
<ul><li><em>Can't skip - you have reviewed all the other ${c.proposal.type.name }s!</em></li></ul>
% endif
<div class="contents"><h3>Review Pages</h3>
<ul>
<%include file="reviewer_sidebar.mako" />
</ul>
</div>
<%include file="view_base.mako" />

<h3>Review</h3>
  <% reviewed_already = False %>
% for x in c.proposal.reviews:
%   if x.reviewer == c.signed_in_person:
<p>You have already reviewered this proposal. To modify your review, ${ h.link_to('click here', url=h.url_for(controller='review', action='edit', id=x.id)) }.</p>
        <% reviewed_already = True %>
        <% break %>
%   endif
% endfor
% if not reviewed_already:
<fieldset>
<legend>
Your opinion on this proposal.
</legend>

<div id="q1">
<p class="label"><span class="mandatory">*</span><b>What score do you give this proposal?</b></p>
<p class="entries">
${ h.radio('review.score', -2, label="-2 (strong reject) I want this proposal to be rejected, and if asked to I will advocate for it to be rejected.") }
<br>
${ h.radio('review.score', -1, label="-1 (reject) I want this proposal to be rejected") }
<br>
${ h.radio('review.score', +1, label="+1 (accept) I want this proposal to be accepted") }
<br>
${ h.radio('review.score', +2, label="+2 (strong accept) I want this proposal to be accepted, and if asked to I will advocate for it to be accepted.") }
</p>
</div>

<div id="q2">
<p class="label">
<span class="mandatory">*</span><b>What stream do you think this talk is most suitable for?</b>
</p>

<p>
${ h.select('review.stream', None, [ (stream.id, stream.name) for stream in c.streams] ) }
</p>
</div>

% if c.proposal.proposal_type_id is not 2:
<div id="q3">
<p class="label">
<b>What miniconf would this talk be most suitable for, if it's not accepted?</b>
</p>

<p>
${ h.select('review.miniconf', None, [ (mc, mc) for mc in miniconfs] ) }
</p>
</div>
% else:
${ h.hiddenfield('review.miniconf') }
% endif

<p class="label"><b>Comments</b> (optional, readable by other reviewers, will not be shown to the submitter)
</p>
<p class="entries">
${ h.textarea('review.comment', size="80x10") }
</p>

</fieldset>

<p>
<span class="mandatory">*</span> - Mandatory field
</p>

<p class="submit">
${ h.submit('submit', 'Submit review and jump to next proposal!') }
</p>

% endif

<p>
% if not c.reviewed_everything:
${ h.link_to('Skip!', url=h.url_for(controller='proposal', action='review', id=c.next_review_id)) } - 
% endif
${ h.link_to('Back to proposal list', url=h.url_for(controller='proposal', action='review_index')) }
</p>
${ h.end_form() }

<%def name="title()">
Reviewing proposal #${ c.proposal.id }, "${ h.truncate(c.proposal.title) }" - ${ caller.title() }
</%def>


