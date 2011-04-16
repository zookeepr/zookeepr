<h3>Review</h3>
<fieldset>
<legend>
Your opinion on this proposal.
</legend>
<div id="q1">
<p><span class="mandatory">*</span><b>What score do you give this proposal?</b>
<br>
${ h.radio('review.score', '-2', label="-2 (strong reject) I want this proposal to be rejected, and if asked to I will advocate for it to be rejected.") }
<br>
${ h.radio('review.score', '-1', label="-1 (reject) I want this proposal to be rejected") }
<br>
${ h.radio('review.score', '+1', label="+1 (accept) I want this proposal to be accepted") }
<br>
${ h.radio('review.score', '+2', label="+2 (strong accept) I want this proposal to be accepted, and if asked to I will advocate for it to be accepted.") }
</p>
</div>

% if len(c.streams) > 1:
<div id="q2">
<p>
<b>What stream do you think this talk is most suitable for?</b>
</p>

<p>
${ h.select('review.stream', None, c.streams ) }

</p>
</div>
% else:
${ h.hidden('review.stream') }
% endif

% if len(h.lca_info['cfp_miniconf_list']) > 1 and c.proposal.proposal_type_id is not 2:
<div id="q3">
<p class="label">
<b>What miniconf would this talk be most suitable for, if it's not accepted?</b>
</p>

<p>
${ h.select('review.miniconf', None, [ (mc, mc) for mc in h.lca_info['cfp_miniconf_list']] ) }
</p>
</div>
% else:
${ h.hidden('review.miniconf') }
% endif


<p><b>Comments</b> (optional, readable by other reviewers, will not be shown to the submitter)

${ h.textarea('review.comment', cols=80, rows=10) }
</p>

</fieldset>


<p>
<span class="mandatory">*</span> - Mandatory field
</p>
