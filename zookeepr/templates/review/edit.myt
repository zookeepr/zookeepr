<h1>Review update</h1>

<h2>#<% c.review.proposal.id %> - "<% c.review.proposal.title %>"</h2>

<div id="review">

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
# Working around a bug in formencode, we need to set the defaults to the
# c.review values
if not defaults:
    defaults = {'review.familiarity': c.review.familiarity,
        'review.technical': c.review.technical,
        'review.experience': c.review.experience,
        'review.coolness': c.review.coolness,
        'review.comment': c.review.comment,
        }
</%init>

<%method title>
Review of <% h.truncate(c.review.proposal.title) %> - <& PARENT:title &>
</%method>
