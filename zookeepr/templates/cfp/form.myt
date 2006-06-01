<div style="width: 400px; margin: auto;">

<fieldset>

<p>First, tell us a bit about yourself.</p>

<p>
<span class="mandatory">*</span>
<label for="person.handle">Username:</label>
<span class="fielddesc"> - the way we'll refer to you</span>
<br />
<% h.text_field('person.handle', c.person.handle) %>
</p>

<p>
<span class="mandatory">*</span>
<label for="person.email_address">Email address:</label><span class="fielddesc"> - this will be the primary way of contacting you</span><br />
<% h.text_field('person.email_address', c.person.email_address) %></p>

<p>
<span class="mandatory">*</span>
<label for="person.password">Password:</label><br />
<% h.password_field('person.password') %></p>

<p>
<span class="mandatory">*</span>
<label for="person.password_confirm">Password (confirm):</label><br />
<% h.password_field('person.password_confirm') %></p>

<p>
<span class="mandatory">*</span>
<span class="fielddesc"> - Mandatory field</span>
</p>
</fieldset>

<fieldset>

<p>Now tell us a bit about your submission.</p>

<p><label for="submission.title">Title:</label><br />
<% h.text_field('submission.title', c.submission.title) %></p>

<p><label for="submission.submission_type">Type:</label><br />
#% for st in c.submissiontypes:
#<% h.radio_button('type', st.name) %>
#<label for="type"><% st.name %></label><br />
#% #endfor
</p>

<p><label for="submission.url">URL:</label><br />
<% h.text_field('submission.url', c.submission.url) %></p>

<p><label for="submission.attachment">File:</label><br />
<% h.file_field('submission.attachment') %></p>

<p><label for="submission.abstract">Abstract:</label><br />
<% h.text_area('submission.abstract') %></p>
</fieldset>

</div>
