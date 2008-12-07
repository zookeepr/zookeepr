<h2>Add a new note</h2>
<&| @zookeepr.lib.form:fill, defaults=defaults, errors=errors &>
<% h.form(h.url(), multipart=True) %>
<& form.myt &>
<% h.end_form() %>
</&>

<%method title>
New note - <& PARENT:title &>
</%method>

<%args>
defaults
errors
</%args>

<%init>
if not defaults:
    defaults = {
        'rego_note.rego': c.id,
        'rego_note.by': c.signed_in_person.id
    }
</%init>
