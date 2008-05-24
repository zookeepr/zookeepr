<&| @zookeepr.lib.form:fill, defaults=defaults, errors=errors &>
<% h.form(h.url(), multipart=True) %>
<& form.myt &>
<% h.submit('Add!') %>
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
