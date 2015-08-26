<h3>Review</h3>
<fieldset>
  <legend>Your opinion on this proposal.</legend>

  <div id="q1">
    <p class="label"><span class="mandatory">*</span><b>What score do you give this proposal?</b></p>
    <p class="entries">
      ${ h.radio('review.score', '-2', label="-2 (strong reject) I want this proposal to be rejected, and if asked to I will advocate for it to be rejected.") }
      <br>
      ${ h.radio('review.score', '-1', label="-1 (reject) I want this proposal to be rejected") }
      <br>
      ${ h.radio('review.score', '1', label="+1 (accept) I want this proposal to be accepted") }
      <br>
      ${ h.radio('review.score', '2', label="+2 (strong accept) I want this proposal to be accepted, and if asked to I will advocate for it to be accepted.") }
      <br>
      ${ h.radio('review.score', '', label="I do not want to see this proposal again, and I don't want to score it") }
    </p>
  </div>

% if len(c.streams) > 1:
  <div id="q2">
    <p class="label"><b>What stream do you think this talk is most suitable for?</b></p>
    <p class="entries">${ h.select('review.stream', None, c.streams ) }</p>
  </div>
% else:
  ${ h.hidden('review.stream') }
% endif

% if len(c.config.get('cfp_miniconf_list')) > 1 and c.proposal.proposal_type_id is not 2:
  <div id="q3">
    <p class="label"><b>What miniconf would this talk be most suitable for, if it's not accepted?</b></p>
    <p class="entries">${ h.select('review.miniconf', None, [ (mc, mc) for mc in c.config.get('cfp_miniconf_list')] ) }</p>
  </div>
% else:
  ${ h.hidden('review.miniconf') }
% endif

  <div id="q4">
    <p class="label"><b>Comments</b> (optional, readable by other reviewers and may be given to the submitter)</p>
    ${ h.textarea('review.comment', cols="80", rows="10") }
  </div>

  <div id="q5">
    <p class="label"><b>Private Comments</b> (optional, readable only by other reviewers, will not be shown to the submitter)</p>
    ${ h.textarea('review.private_comment', cols="80", rows="10") }
  </div>
</fieldset>

<p>
<span class="mandatory">*</span> - Mandatory field
</p>
