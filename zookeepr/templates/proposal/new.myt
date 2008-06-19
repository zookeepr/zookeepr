<h1>New Proposal</h1>

<&| @zookeepr.lib.form:fill, defaults=defaults, errors=errors &>

<% h.form(h.url(), multipart=True) %>
<& form.myt &>
<% h.submitbutton("New") %>
<% h.end_form() %>

</&>

#<% h.link_to('Back', url=h.url(action='index')) %>

<%args>
defaults
errors
</%args>
