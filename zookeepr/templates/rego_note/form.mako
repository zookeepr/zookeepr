<fieldset>

<p class="label">
<label for="rego_note.url">Registration ID:</label>
</p><p class="entries">
${ h.text('rego_note.rego_id', size=10) }
</p>
<p class="note">Enter the registration ID you wish to append this note to. (${ h.link_to('See registration list', h.url_for(controller='registration', action='index')) })</p>

<p class="label">
<label for="rego_note.body">Note:</label>
</p><p class="entries">
${ h.textarea('rego_note.note', cols="70", rows="6") }
</p>

<p class="label">
<label for="rego_note.url">By ID:</label>
</p><p class="entries">
${ h.text('rego_note.by_id', size=10) }
</p>
<p class="note">Who is this note posted by (defaults to your ID)? (${ h.link_to('See person list', h.url_for(controller='person', action='index')) })</p>

<p>
${ h.submit('submit', 'Save') }
</p>
</fieldset>

