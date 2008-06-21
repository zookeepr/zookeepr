<&| @zookeepr.lib.form:fill, defaults=defaults, errors=errors &>

<% h.form(url=h.url(), multipart=True) %>

<p><label for="attachment">Attach a file:</label>
<br>
<% h.file_field('attachment', size=50) %>

<br>

<% h.submitbutton('Upload') %>
</p>
<% h.end_form() %>

</&>

<%args>
defaults
errors
</%args>
