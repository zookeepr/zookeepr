<p>
<strong>The Call for Participation is now closed!</strong>
</p>

<&| @zookeepr.lib.form:fill, defaults=defaults, errors=errors &>
<% h.form(h.url(), multipart=True) %>
<& form.myt &>
<% h.submit('Participate!') %>
<% h.end_form() %>
</&>

<%method title>
Call for Participation - <& PARENT:title &>
</%method>

<%args>
defaults
errors
</%args>
