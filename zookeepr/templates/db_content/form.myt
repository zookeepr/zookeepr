<fieldset>

<p class="label">
<span class="mandatory">*</span>
<label for="db_content.title">Title:</label>
</p><p class="entries">
<% h.textfield('db_content.title', size=60) %>
</p><p class="note">
The page title
</p>

<p class="label"><span class="mandatory">*</span><span class="publishable">&#8224;</span><label>Content Type:</label></p>
<p class="entries">
% for st in c.db_content_types:
<label><% h.radio('db_content.type', st.id) %> <% st.name |h %></label><br>
% #endfor
</p>

<p class="label">
<label for="db_content.url">URL:</label>
</p><p class="entries">
<% h.textfield('db_content.url', size=60) %>
</p><p class="note">
The URL after the linux.conf.au/ that this page should be rendered for. EG: 'about/linux'<br>
You don't have to supply a URL as content is still accessible via ID's. It is recommended not to create a URL alias for news items.
</p>

<p class="label">
<span class="mandatory">*</span>
<label for="db_content.body">Body:</label>
</p><p class="entries">
<% h.textarea('db_content.body', size="70x6") %>
</p><p class="note">
The HTML rendered body. Please surround by &lt;p&gt; tags when appropriate. Use &lt;h3&gt;'s to automatically create a "contents" section.<br>
For news articles you can place a <!--break--> statement to separate the entire body from the preview on the news page.
</p>
<p>
<% h.submitbutton('Save') %>
</p>
</fieldset>

