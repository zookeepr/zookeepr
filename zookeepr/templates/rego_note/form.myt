<fieldset>

<p class="label">
<label for="db_content.url">Registration ID:</label>
</p><p class="entries">
<% h.textfield('rego_note.rego', size=10) %>
</p>
<p class="note">Enter the registration ID you wish to append this note to. (<% h.link_to('See registration list', h.url(controller='registration', action='index')) %>)</p>

<p class="label">
<label for="db_content.body">Note:</label>
</p><p class="entries">
<% h.textarea('rego_note.note', size="70x6") %>
</p>


<p class="label">
<label for="db_content.url">By ID:</label>
</p><p class="entries">
<% h.textfield('rego_note.by', size=10) %>
</p>
<p class="note">Who is this note posted by (defaults to your ID)? (<% h.link_to('See person list', h.url(controller='person', action='index')) %>)</p>


<p>
<% h.submitbutton('Save') %>
</p>
</fieldset>

