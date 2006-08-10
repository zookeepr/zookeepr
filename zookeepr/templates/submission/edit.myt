<h2>Edit submission <% c.submission.id %></h2>

<div id="submission">

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
# Working around a bug in formencode, we need to set the defaults to the c.submission
# values
if not defaults:
	defaults = {'submission.title': c.submission.title,
		    'submission.type': c.submission.type.id,
		    'submission.abstract': c.submission.abstract,
                    'submission.experience': c.submission.experience,
                    'submission.url': c.submission.url,
                   }
</%init>
