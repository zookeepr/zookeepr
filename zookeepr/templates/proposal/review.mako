<%inherit file="view_base.mako" />
<%
# warning: this list must match the one in ../review/form.mako
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

<%def name="toolbox_extra()">
  ${ parent.toolbox_extra() }
% if c.next_review_id:
  <li>${ h.link_to('Skip!', url=h.url_for(controller='proposal', action='review', id=c.next_review_id)) }</li>
% endif
</%def>


<%def name="heading()">
  Proposal Review - #${ c.proposal.id } - ${ c.proposal.title | h }
</%def>

${ h.form(h.url_for()) }

% if c.next_review_id:
<ul><li>${ h.link_to('Skip!', url=h.url_for(controller='proposal', action='review', id=c.next_review_id)) }</li></ul>
% else:
<ul><li><em>Can't skip - you have reviewed all the other ${c.proposal.type.name }s!</em></li></ul>
% endif

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
${ h.radio('review.score', '-2', label="-2 (strong reject) I want this proposal to be rejected, and if asked to I will advocate for it to be rejected.") }
<br>
${ h.radio('review.score', '-1', label="-1 (reject) I want this proposal to be rejected") }
<br>
${ h.radio('review.score', '+1', label="+1 (accept) I want this proposal to be accepted") }
<br>
${ h.radio('review.score', '+2', label="+2 (strong accept) I want this proposal to be accepted, and if asked to I will advocate for it to be accepted.") }
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
${ h.hidden('review.miniconf') }
% endif

<p class="label"><b>Comments</b> (optional, readable by other reviewers, will not be shown to the submitter)
</p>
<p class="entries">
${ h.textarea('review.comment', cols="80", rows="10") }
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
% if c.next_review_id:
${ h.link_to('Skip!', url=h.url_for(controller='proposal', action='review', id=c.next_review_id)) } - 
% endif
${ h.link_to('Back to proposal list', url=h.url_for(controller='proposal', action='review_index')) }
</p>
${ h.end_form() }

<%def name="title()">
Reviewing proposal #${ c.proposal.id } - ${ parent.title() }
</%def>


