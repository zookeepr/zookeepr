<p>
<label for="rego_note.rego">Registration ID:</label>
${ h.text('rego_note.rego', size=10) }
</p>
<p class="note">Enter the registration ID you wish to append this note to. (${ h.link_to('See registration list', h.url_for(controller='registration', action='index')) })</p>

<p>
<label for="rego_note.note">Note:</label><br />
${ h.textarea('rego_note.note', cols="70", rows="6") }
</p>

<p>
<label for="rego_note.block">Block:</label><br />
${ h.checkbox('rego_note.block') }
</p>
<p class="note">Setting this flag will cause this note to pop-up at checkin</p>

<p>
<label for="rego_note.by">By ID:</label>
${ h.text('rego_note.by', size=10) }
</p>

<p class="note">Who is this note posted by (defaults to your ID)? (${ h.link_to('See person list', h.url_for(controller='person', action='index')) })</p>

