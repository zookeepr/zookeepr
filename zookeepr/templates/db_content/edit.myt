<h2>Edit page</h2>
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
if not defaults:
    defaults = {
        'db_content.title': c.db_content.title,
        'db_content.url': c.db_content.url,
        'db_content.body': c.db_content.body,
    }
</%init>
