<h3>Review</h3>
<fieldset>
<legend>
Your opinion on this funding application.
</legend>
<div id="q1">
<p><span class="mandatory">*</span><b>What score do you give this application?</b>
<br>
${ h.radio('review.score', 'null', label="Abstain") }
<br>
${ h.radio('review.score', '-2', label="-2 (strong reject) I want this funding application to be rejected, and if asked to I will advocate for it to be rejected.") }
<br>
${ h.radio('review.score', '-1', label="-1 (reject) I want this funding application to be rejected") }
<br>
${ h.radio('review.score', '+1', label="+1 (accept) I want this funding application to be accepted") }
<br>
${ h.radio('review.score', '+2', label="+2 (strong accept) I want this funding application to be accepted, and if asked to I will advocate for it to be accepted.") }
</p>
</div>

<p><b>Comments</b> (optional, readable by other reviewers, will not be shown to the submitter)

${ h.textarea('review.comment', cols=80, rows=10) }
</p>

</fieldset>


<p>
<span class="mandatory">*</span> - Mandatory field
</p>
