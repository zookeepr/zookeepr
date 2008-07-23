<h3>Review</h3>
<fieldset>
<legend>
Your opinion on this proposal.
</legend>
<div id="q1">
<p><span class="mandatory">*</span>1. What score do you give this proposal?
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
<span class="mandatory">*</span>2. What stream do you think this talk is most suitable for?
</p>

<p>
<% h.select('review.stream', option_tags=h.options_for_select_from_objects(c.streams, 'name', 'id')) %>
</p>
</div>

<p class="label">
3. What miniconf would this talk be most suitable for, if it's not accepted?
</p>

<p>
<% h.select('review.miniconf', option_tags=h.options_for_select( [ [mc, mc]
for mc in miniconfs] ) ) %>
</p>


<p>4. Comments (optional, readable by other reviewers, will not be shown to the submitter)

<% h.textarea('review.comment', size="80x10") %>
</p>

</fieldset>

<p>
<span class="mandatory">*</span> - Mandatory field
</p>
<%init>
# warning: this list must match the one in ../proposal/review.myt
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
