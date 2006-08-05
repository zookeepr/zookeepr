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
if not defaults:
	defaults = {'submission.title': c.submission.title,
		    'submission.submission_type_id': c.submission.submission_type_id,
		    'submission.abstract': c.submission.abstract,
                    'submission.experience': c.submission.experience,
                    'submission.url': c.submission.url,
                   }
</%init>
