<h2>Proposal Review - #<% c.proposal.id %></h2>

<&| @zookeepr.lib.form:fill, defaults=defaults, errors=errors &>

<% h.form(h.url_for()) %>

<p>
% if c.next_review_id:
<% h.link_to('Skip!', url=h.url(controller='proposal', action='review', id=c.next_review_id)) %> - 
% #endif
<% h.link_to('Back to proposal list', url=h.url(controller='proposal', action='review_index')) %>
</p>

<& view.myt &>

<h3>Review</h3>
<fieldset>
<legend>
Your opinion on this proposal.
</legend>

<div id="q1">
<p class="label"><span class="mandatory">*</span>1. What score do you give this proposal?</p>
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
<span class="mandatory">*</span>2. What stream do you think this talk is most suitable for?
</p>

<p>
<% h.select('review.stream', option_tags=h.options_for_select_from_objects(c.streams, 'name', 'id')) %>
</p>
</div>

<div id="q3">
<p class="label">
3. What miniconf would this talk be most suitable for, if it's not accepted?
</p>

<p>
<% h.select('review.miniconf', option_tags=h.options_for_select( [ [mc, mc]
for mc in miniconfs] ) ) %>
</p>
</div>
<p class="label">Comments (optional, readable by other reviewers, will not be shown to the submitter)
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

% if c.next_review_id:
<p><% h.link_to('Skip!', url=h.url(controller='proposal', action='review', id=c.next_review_id)) %></p>
% #endif
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
  '',
  '(none)',
  'Debian',
  'Distro Summit',
  'Education',
  'Embedded',
  'Fedora',
  'Gaming',
  'Gentoo',
  'Gnome',
  'Kernel',
  'LinuxChix',
  'MySQL',
  'Security',
  'SysAdmin',
  'Virtualisation',
  'Wireless',
)
</%init>
