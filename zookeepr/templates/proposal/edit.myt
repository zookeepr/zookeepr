<h2>Edit proposal <% c.proposal.id %></h2>

<div id="proposal">

<&| @zookeepr.lib.form:fill, defaults=defaults, errors=errors &>

<% h.form(h.url()) %>
<& form.myt &>
<% h.submit('Update') %>
<% h.end_form() %>

</&>

</div>

<%args>
defaults
errors
</%args>

<%init>
# Working around a bug in formencode, we need to set the defaults to the c.proposal
# values
#
# 13.6.2007 (IM between sabik & johnf):
# (17:19:32) sabik: Would you remember the nature of the bug and/or how I
# need to take it into account when I change the form?
# (17:21:29) johnf: jaq fixed that but I know whenever I've
# changed a form I've had to add its elements to that it of code
# (17:22:09) sabik: OK, I guess I can just do that too...

if not defaults and c.proposal:
    defaults = {
            'proposal.title': c.proposal.title,
            'proposal.abstract': c.proposal.abstract,
            'person.experience': c.person.experience,
            'person.bio': c.person.bio,
            'proposal.url': c.proposal.url,
    }
    if c.proposal.type:
        defaults['proposal.type'] = c.proposal.type.id
    if c.proposal.assistance:
        defaults['proposal.assistance'] = c.proposal.assistance.id

</%init>
