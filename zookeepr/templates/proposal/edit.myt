<h2>Edit proposal <% c.proposal.id %></h2>

<div id="proposal">

<&| @zookeepr.lib.form:fill, defaults=defaults, errors=errors &>

<% h.form(h.url()) %>
<& form.myt &>

<p class="submit">
<% h.submit('Update') %>
</p>

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
