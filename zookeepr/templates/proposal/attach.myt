<&| @zookeepr.lib.form:fill, defaults=defaults, errors=errors &>

<% h.form(url=h.url()) %>

<label for="attachment">Attach a file</label>
<br />
<% h.file_field('attachment', size=50) %>

<br />
<br />

<% h.submit('Ok!') %>

<% h.end_form() %>

</&>

<%args>
defaults
errors
</%args>
