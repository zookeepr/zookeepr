<h2>Add a new page</h2>
<&| @zookeepr.lib.form:fill, defaults=defaults, errors=errors &>
<% h.form(h.url(), multipart=True) %>
<& form.myt &>
<% h.end_form() %>
</&>

<%method title>
New page - <& PARENT:title &>
</%method>

<%args>
defaults
errors
</%args>

<%init>
</%init>
