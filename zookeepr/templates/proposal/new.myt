<h2>New proposal</h2>

<&| @zookeepr.lib.form:fill, defaults=defaults, errors=errors &>

<% h.form(h.url()) %>
<& form.myt &>
<% h.submit("New") %>
<% h.end_form() %>

</&>

#<% h.link_to('Back', url=h.url(action='index')) %>

<%args>
defaults
errors
</%args>
