<div style="width: 600px; margin: auto;">

<fieldset>

<p>First, tell us a bit about yourself.</p>

<p>
<span class="mandatory">*</span>
<label for="registration.fullname">Your name:</label>
<% h.text_field('registration.fullname', c.registration.fullname, size=40) %>
<br />
</p>

<p>
<span class="mandatory">*</span>
<label for="registration.email_address">Email address:</label>
<% h.text_field('registration.email_address', c.registration.email_address, size=40) %>
<br />
<span class="fielddesc"> - this will be the primary way of contacting you</span>
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

<p>Now tell us a bit about your proposal:</p>

<p><label for="proposal.title">Title:</label>
<% h.text_field('proposal.title', c.proposal.title, size=50) %>
<br />
<span class="fielddesc">e.g. the name of your paper, or talk title.</span>
</p>

<p><label>Proposal Type:</label>
<br />
% for st in c.cfptypes:
<% h.radio_button('proposal.type', st.id) %>
<label for="proposal.type"><% st.name |h %></label><br />
% #endfor
<span class="fielddesc">What sort of proposal is this?</span>
</p>

<p><label for="proposal.url">Project URL:</label>
<% h.text_field('proposal.url', c.proposal.url, size=50) %>
<br />
<span class="fielddesc">if your proposal has a project URL, specify it here so the review committee can find out more about your proposal.</span>
</p>

<p><label for="proposal.attachment">Attach a file:</label>
<% h.file_field('proposal.attachment', size=50) %>
<br />
<span class="fielddesc">If you are submitting a paper for peer review, please upload it here.</span>
</p>

<p><label for="proposal.abstract">Abstract:</label>
<span class="fielddesc">Please write here a summary of your proposal.</span>
<br />
<% h.text_area('proposal.abstract', cols=50, rows=10) %>
</p>

<p><label for="proposal.experience">Experience:</label>
<span class="fielddesc">Have you had any experience presenting this proposal elsewhere?  If so, we'd like to know.</span>
<br />
<% h.text_area('proposal.experience', cols=50, rows=5) %>
</p>

<p><label>Need travel assistance?</label>
<% h.check_box('proposal.assistance') %>
<span class="fielddesc">Travel assistance is available to speakers who qualify.  If you think you need it, please let us know.</span>
</p>

</fieldset>

</div>
