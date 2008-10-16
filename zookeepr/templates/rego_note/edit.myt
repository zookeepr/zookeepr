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
        'rego_note.rego': c.rego_note.rego.id,
        'rego_note.note': c.rego_note.note,
        'rego_note.by': c.rego_note.by.id
    }
</%init>
