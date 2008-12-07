<h1>Edit role</h1>

<&| @zookeepr.lib.form:fill, defaults=defaults, errors=errors &>
<% h.form(h.url(id=c.role.id)) %>
<& form.myt &>
<p><% h.submitbutton('Update') %> - <% h.link_to('back', url=h.url(action='index', id=None)) %></p>
<% h.end_form() %>
</&>
<%args>
defaults
errors
</%args>
<%init>
if not defaults and c.role:
    defaults = {
        'role.name' : c.role.name
        }
</%init>
