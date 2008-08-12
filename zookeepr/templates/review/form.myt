<h3>Review</h3>
<fieldset>
<legend>
Your opinion on this proposal.
</legend>
<div id="q1">
<p><span class="mandatory">*</span><b>What score do you give this proposal?</b>
<br>
<% h.radio('review.score', -2, "-2 (strong reject) I want this proposal to be rejected, and if asked to I will advocate for it to be rejected.") %>
<br>
<% h.radio('review.score', -1, "-1 (reject) I want this proposal to be rejected") %>
<br>
<% h.radio('review.score', +1, "+1 (accept) I want this proposal to be accepted") %>
<br>
<% h.radio('review.score', +2, "+2 (strong accept) I want this proposal to be accepted, and if asked to I will advocate for it to be accepted.") %>
</p>
</div>

<div id="q2">
<p>
<span class="mandatory">*</span><b>What stream do you think this talk is most suitable for?</b>
</p>

<p>
<% h.select('review.stream', option_tags=h.options_for_select_from_objects(c.streams, 'name', 'id')) %>
</p>
</div>

% if c.proposal.proposal_type_id is not 2:
<div id="q3">
<p class="label">
<b>What miniconf would this talk be most suitable for, if it's not accepted?</b>
</p>

<p>
<% h.select('review.miniconf', option_tags=h.options_for_select( [ [mc, mc]
for mc in miniconfs] ) ) %>
</p>
</div>
% else:
<% h.hiddenfield('review.miniconf') %>
% #endif


<p><b>Comments</b> (optional, readable by other reviewers, will not be shown to the submitter)

<% h.textarea('review.comment', size="80x10") %>
</p>

</fieldset>

<p>
<span class="mandatory">*</span> - Mandatory field
</p>
<%init>
# warning: this list must match the one in ../proposal/review.myt
miniconfs = (
  '(none)',
  'Debian',
  'Free as in Freedom',
  'Functional Programming',
  'Gaming',
  'Gentoo Down Under',
  'GNOME.conf.au',
  'High Performance Linix BoF'
  'Joomla!',
  'Lifehacker',
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
</%init>
