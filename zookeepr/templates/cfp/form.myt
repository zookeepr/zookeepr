<div style="width: 600px; margin: auto;">

<fieldset>

<p>First, tell us a bit about yourself.</p>

<p>
<span class="mandatory">*</span>
<label for="registration.email_address">Email address:</label>
<% h.text_field('registration.email_address', c.registration.email_address, size=40) %>
<br />
<span class="formdesc"> - this will be the primary way of contacting you</span>
</p>

<p>
<span class="mandatory">*</span>
<label for="registration.password">Password:</label><br />
<% h.password_field('registration.password') %></p>

<p>
<span class="mandatory">*</span>
<label for="registration.password_confirm">Password (confirm):</label><br />
<% h.password_field('registration.password_confirm') %></p>

<p>
<span class="mandatory">*</span>
<span class="fielddesc"> - Mandatory field</span>
</p>
</fieldset>

<fieldset>

<p>Now tell us a bit about your submission:</p>

<p><label for="submission.title">Title:</label>
<% h.text_field('submission.title', c.submission.title, size=50) %>
<br />
<span class="formdesc">e.g. the name of your paper, or talk title.</span>
</p>

<p><label>Submission Type:</label>
<br />
% for st in c.cfptypes:
<% h.radio_button('submission.type', st.id) %>
<label for="submission.type"><% st.name |h %></label><br />
% #endfor
<span class="formdesc">What sort of submission is this?</span>
</p>

<p><label for="submission.url">Project URL:</label>
<% h.text_field('submission.url', c.submission.url, size=50) %>
<br />
<span class="formdesc">if your submission has a project URL, specify it here so the review committee can find out more about your submission.</span>
</p>

<p><label for="submission.attachment">Attach a file:</label>
<% h.file_field('submission.attachment', size=50) %>
<br />
<span class="formdesc">If you are submitting a paper for peer review, please upload it here.</span>
</p>

<p><label for="submission.abstract">Abstract:</label>
<span class="formdesc">Please write here a summary of your submission.</span>
<br />
<% h.text_area('submission.abstract', cols=50, rows=10) %>
</p>

<p><label for="submission.experience">Experience:</label>
<span class="formdesc">Have you had any experience presenting this submission elsewhere?  If so, we'd like to know.</span>
<br />
<% h.text_area('submission.experience', cols=50, rows=5) %>
</p>

<p><label>Need travel assistance?</label>
<% h.check_box('submission.assistance') %>
<span class="formdesc">Travel assistance is available to speakers who qualify.  If you think you need it, please let us know.</span>
</p>

</fieldset>

</div>
