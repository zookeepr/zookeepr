<h2>Add a new page</h2>

<fieldset>

<p class="label">
<span class="mandatory">*</span>
<label for="db_content.title">Title:</label>
</p><p class="entries">
<% h.text_field('db_content.title', size=60) %>
</p><p class="note">
The page title
</p>

<p class="label">
<span class="mandatory">*</span>
<label for="db_content.url">URL:</label>
</p><p class="entries">
<% h.text_field('db_content.url', size=60) %>
</p><p class="note">
The URL after the linux.conf.au/ that this page should be rendered for. EG: 'about/linux'
</p>

<p class="label">
<span class="mandatory">*</span>
<label for="db_content.body">Body:</label>
</p><p class="entries">
<% h.text_area('db_content.body', size="70x6") %>
</p><p class="note">
The HTML rendered body.
</p>
<% h.submit('Add!') %>
</fieldset>

