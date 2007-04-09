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

<%init>
# Working around a bug in formencode, we need to set the defaults to the c.proposal
# values
if not defaults:
    defaults = {
        'person.experience': c.person.experience,
        'person.bio': c.person.bio
    }
</%init>
