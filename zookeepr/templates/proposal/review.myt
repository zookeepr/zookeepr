<h2>Proposal Review - #<% c.proposal.id %></h2>

<&| @zookeepr.lib.form:fill, defaults=defaults, errors=errors &>

<% h.form(h.url_for()) %>

% if c.next_review_id:
<ul><li><% h.link_to('Skip!', url=h.url(controller='proposal', action='review', id=c.next_review_id)) %></li></ul>
% #endif
<div class="contents"><h3>Review Pages</h3>
<ul>
<li><a href="/review/help">How to review</a></li>
<li><% h.link_to('Review proposals', url=h.url(controller='proposal', action='review_index')) %></li>
<li><% h.link_to('Your reviews', url=h.url(controller='review', action='index')) %></li>
<li><% h.link_to('Summary of proposals', url=h.url(controller='proposal', action='summary')) %></li>
<li><% h.link_to('Reviewer summary', url=h.url(controller='review', action='summary')) %></li>
</ul>
</div>
<& view.myt &>

<h3>Review</h3>
% print c.signed_in_person.reviews
% if c.signed_in_person in [x.reviewer for x in c.proposal.reviews]:
<p>You have already reviewered this proposal. To modify your review, <% h.link_to('click here', url=h.url(controller='review', action='edit', id=x.id)) %>.</p>
% else:
<fieldset>
<legend>
Your opinion on this proposal.
</legend>

<div id="q1">
<p class="label"><span class="mandatory">*</span><b>What score do you give this proposal?</b></p>
<p class="entries">
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
<p class="label">
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

<p class="label"><b>Comments</b> (optional, readable by other reviewers, will not be shown to the submitter)
</p>
<p class="entries">
<% h.textarea('review.comment', size="80x10") %>
</p>

</fieldset>

<p>
<span class="mandatory">*</span> - Mandatory field
</p>

<p class="submit">
<% h.submitbutton('Submit review and jump to next proposal!') %>
</p>

% #endif

<p>
% if c.next_review_id:
<% h.link_to('Skip!', url=h.url(controller='proposal', action='review', id=c.next_review_id)) %> - 
% #endif
<% h.link_to('Back to proposal list', url=h.url(controller='proposal', action='review_index')) %>
</p>
<% h.end_form() %>

</&>

<%method title>
Reviewing proposal #<% c.proposal.id %>, "<% h.truncate(c.proposal.title) %>" - <& PARENT:title &>
</%method>

<%args>
defaults
errors
</%args>
<%init>
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
</%init>
