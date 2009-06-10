<fieldset>

<p class="label">
<span class="mandatory">*</span>
<label for="db_content.title">Title:</label>
</p><p class="entries">
${ h.text('db_content.title', size=60) }
</p>
<ul class="note"><li>To feature news items simply place (via FTP) a png image in the /featured/ folder with the same name as the title in computer friendly form. For example "Welcome to LCA!" will look for "/featured/welcome_to_lca.png" and if it exists the item will appear down the side of the home page.</li>
<li>To make a news item a major feature (i.e above the menu bar), create a folder in /featured/ with parts 1.png, 2.png and 3.png. Using the above example the images would go into "/featured/welcome_to_lca/1.png"</li>
</ul>

<p class="label"><span class="mandatory">*</span><span class="publishable">&#8224;</span><label>Content Type:</label></p>
<p class="entries">
% for st in c.db_content_types:
<label>${ h.radio('db_content.type', st.id) } ${ st.name |h }</label><br>
% endfor
</p>

<p class="label">
<label for="db_content.url">URL:</label>
</p><p class="entries">
${ h.text('db_content.url', size=60) }
</p>
<ul class="note"><li>For pages and news items this is the URL after the linux.conf.au/ that this page should be rendered for. EG: 'about/linux'.<br>
It is not mandatory supply a URL as content is still accessible via ID's. It is recommended not to create a URL alias for news items.</li>
<li>For "In the press" this is the URL you want the item to link to.</li></ul>

<p class="label">
<label for="db_content.body">Body:</label>
</p><p class="entries">
${ h.textarea('db_content.body', cols="80", rows="40") }
</p>
<ul class="note"><li>The HTML rendered body. Please surround by &lt;p&gt; tags when appropriate. Use &lt;h3&gt;'s to automatically create a "contents" section.</li>
<li>For news articles you can place a &lt;!--break--&gt; statement to separate the entire body from the preview on the news page.</li>
<li>For in the press this becomes the comment under the link.</li></ul>
<p>
${ h.submit("submit", "Save",) }
</p>
</fieldset>

