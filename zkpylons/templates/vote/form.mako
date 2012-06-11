<p>
<label for="vote.rego">Cast your vote. You may use more than one of your vote tokens for this event:</label>
${ h.text('vote.vote_value', size=10) }
</p>
<p class="comment">You may enter an optional comment which <b>will be made public</b>. Consider the conference code of conduct when making a comment. </p>

<p>
<label for="vote.comment">Comment:</label><br />
${ h.textarea('vote.comment', cols="70", rows="6") }
${ h.hidden('vote.event_id')}
${ h.hidden('vote.rego_id')}
</p>


