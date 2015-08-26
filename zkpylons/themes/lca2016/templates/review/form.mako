<h3>Review</h3>
<fieldset>
  <legend>Your opinion on this proposal.</legend>

    <div class="row form-group">
        <label for="reviewscore" class="col-sm-2 control-label">What score do you give this proposal?</label>
        <div class="col-sm-10">
            <div class="radio">
                ${ h.radio('review.score', '-2', label="-2 (strong reject) I want this proposal to be rejected, and if asked to I will advocate for it to be rejected.") }
            </div>
            <div class="radio">
                ${ h.radio('review.score', '-1', label="-1 (reject) I want this proposal to be rejected") }
            </div>
            <div class="radio">
                ${ h.radio('review.score', '1', label="+1 (accept) I want this proposal to be accepted") }
            </div>
            <div class="radio">
              ${ h.radio('review.score', '2', label="+2 (strong accept) I want this proposal to be accepted, and if asked to I will advocate for it to be accepted.") }
            </div>
            <div class="radio">
                ${ h.radio('review.score', '', label="I do not want to see this proposal again, and I don't want to score it") }
            </div>
        </div>
    </div>

% if len(c.streams) > 1:
  <div class="row form-group">
        <label for="reviewstream" class="col-sm-2 control-label">What stream do you think this talk is most suitable for?</label>
        <p class="entries">${ h.select('review.stream', None, c.streams ) }</p>
  </div>
% else:
  ${ h.hidden('review.stream') }
% endif

% if len(c.config.get('cfp_miniconf_list')) > 1 and c.proposal.proposal_type_id is not 2:
  <div class="row form-group">
        <label for="reviewminiconf" class="col-sm-2 control-label">What miniconf would this talk be most suitable for, if it's not accepted?</label>
        <p class="entries">${ h.select('review.miniconf', None, [ (mc, mc) for mc in c.config.get('cfp_miniconf_list')] ) }</p>
  </div>
% else:
  ${ h.hidden('review.miniconf') }
% endif

    <div class="row form-group"> 
      <div class="textarea">
        <label for="reviewcomment" class="col-sm-2 control-label">Comments</label>
        <textarea class="form-control" id="reviewcomment" placeholder="Readable by other reviewers and may be given to the submitter (Optional but recommended)" name="review.comment" rows="10" cols="80"></textarea>
      </div>
    </div>

    <div class="row form-group"> 
      <div class="textarea">
        <label for="reviewprivate_comment" class="col-sm-2 control-label">Private Comments</label>
        <textarea class="form-control" id="reviewprivate_comment" placeholder="Readable only by other reviewers, will NOT be shown to the submitter (Optional)" name="review.private_comment" rows="10" cols="80"></textarea>
      </div>
    </div>

</fieldset>
