<div style="width: 600px; margin: auto;">

<fieldset>

<p>First, tell us a bit about yourself.</p>

<p>
<span class="mandatory">*</span>
<label for="cfp.email_address">Email address:</label><span class="fielddesc"> - this will be the primary way of contacting you</span><br />
<% h.text_field('cfp.email_address', c.cfp.email_address, size=40) %></p>

<p>
<span class="mandatory">*</span>
<label for="cfp.password">Password:</label><br />
<% h.password_field('cfp.password') %></p>

<p>
<span class="mandatory">*</span>
<label for="cfp.password_confirm">Password (confirm):</label><br />
<% h.password_field('cfp.password_confirm') %></p>

<p>
<span class="mandatory">*</span>
<span class="fielddesc"> - Mandatory field</span>
</p>
</fieldset>

<fieldset>

<p>Now tell us a bit about your submission:</p>

<p><label for="cfp.title">Title:</label><br />
<% h.text_field('cfp.title', c.cfp.title, size=50) %>
E.g. the name of your paper, or talk title.
</p>

<p><label>Submission Type:</label><br />
% for st in c.cfptypes:
<% h.radio_button('cfp.type', st.id) %>
<label for="cfp.type"><% st.name |h %></label><br />
% #endfor
What sort of submission is this?
</p>

<p><label for="cfp.url">Project URL:</label><br />
<% h.text_field('cfp.url', c.cfp.url, size=50) %>
If your submission has a project URL, list it here so the review committee can find out more about your submission.
</p>

<p><label for="cfp.attachment">Attach a file:</label><br />
<% h.file_field('cfp.attachment', size=50) %>
If you are submitting a paper for peer review, please upload it here.
</p>

<p><label for="cfp.abstract">Abstract:</label><br />
<% h.text_area('cfp.abstract', cols=50, rows=10) %>
Please write here a summary of your submission.
</p>

<p><label for="cfp.experience">Experience:</label><br />
<% h.text_area('cfp.experience', cols=50, rows=5) %>
Have you had any experience presenting this submission elsewhere?  If so, we'd like to know.
</p>

<p><label>Need travel assistance?</label>
<% h.check_box('cfp.assistance') %>
Travel assistance is available to some speakers who qualify.  If you think you need it, please let us know.
</p>

</fieldset>

</div>
