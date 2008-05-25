<fieldset>

<p class="label">
<span class="mandatory">*</span>
<label for="db_content.title">Title:</label>
</p><p class="entries">
<% h.textfield('db_content.title', size=60) %>
</p><p class="note">
The page title
</p>

<p class="label">
<span class="mandatory">*</span>
<label for="db_content.url">URL:</label>
</p><p class="entries">
<% h.textfield('db_content.url', size=60) %>
</p><p class="note">
The URL after the linux.conf.au/ that this page should be rendered for. EG: 'about/linux'
</p>

<p class="label">
<span class="mandatory">*</span>
<label for="db_content.body">Body:</label>
</p><p class="entries">
<% h.textarea('db_content.body', size="70x6") %>
</p><p class="note">
The HTML rendered body. Please surround by &lt;p&gt; tags when appropriate.
</p>
<p>
<% h.submitbutton('Save') %>
</p>
</fieldset>

