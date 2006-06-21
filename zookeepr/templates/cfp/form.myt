<div style="width: 600px; margin: auto;">

<fieldset>

<p>First, tell us a bit about yourself.</p>

#<p>
#<span class="mandatory">*</span>
#<label for="cfp.handle">Username:</label>
#<span class="fielddesc"> - the way we'll refer to you</span>
#<br />
#<% h.text_field('cfp.handle', c.cfp.handle) %>
#</p>

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

<p>Now tell us a bit about your cfp.</p>

<p><label for="cfp.title">Title:</label><br />
<% h.text_field('cfp.title', c.cfp.title, size=50) %></p>

<p><label>Type:</label><br />
% for st in c.cfptypes:
<% h.radio_button('cfp.type', st.id) %>
#% 	print type(st.name)
<label for="cfp.type"><% st.name |h %></label><br />
% #endfor
</p>

<p><label for="cfp.url">URL:</label><br />
<% h.text_field('cfp.url', c.cfp.url, size=50) %></p>

<p><label for="cfp.attachment">File:</label><br />
<% h.file_field('cfp.attachment', size=50) %></p>

<p><label for="cfp.abstract">Abstract:</label><br />
<% h.text_area('cfp.abstract', cols=50, rows=10) %></p>

<p><label for="cfp.experience">Experience:</label><br />
<% h.text_area('cfp.experience', cols=50, rows=5) %></p>

</fieldset>

</div>
