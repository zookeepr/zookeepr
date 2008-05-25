<h2>Edit page</h2>
<% `defaults` |h%>
<&| @zookeepr.lib.form:fill, defaults=defaults, errors=errors &>
<% h.form(h.url(), multipart=True) %>
<& form.myt &>
<% h.end_form() %>
</&>

<%method title>
Edit page - <& PARENT:title &>
</%method>

<%args>
defaults
errors
</%args>

<%init>
</%init>
