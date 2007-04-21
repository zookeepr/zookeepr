<&| @zookeepr.lib.form:fill, defaults=defaults, errors=errors &>
<h1>Propose a Mini-conf</h1>
<h2>About yourself</h2>

<p><em>Note: These are common for all your proposals, both mini-confs and papers.</em></p>


<% h.form(h.url(), multipart=True) %>
<table class="form" summary="submission form">
<& form_mini.myt &>
</table>

	<span class="submit"><% h.submit('Submit!') %></span>
<% h.end_form() %>
</&>

<%method title>
Call for Mini-confs - <& PARENT:title &>
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
