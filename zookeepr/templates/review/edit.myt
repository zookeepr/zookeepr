<&| @zookeepr.lib.form:fill, defaults=defaults, errors=errors &>
<h1>Review update</h1>

<& ../proposal/view.myt &>

<div id="review">
<% h.form(h.url()) %>
<& form.myt &>
<% h.submitbutton('Update') %>
<% h.end_form() %>
</div>

</&>
<%args>
defaults
errors
</%args>

<%init>
# Working around a bug in formencode, we need to set the defaults to the
# c.review values
c.proposal = c.review.proposal
if not defaults:
    defaults = {'review.score': c.review.score,
        'review.comment': c.review.comment,
        }
</%init>

<%method title>
Review of <% h.truncate(c.review.proposal.title) %> - <& PARENT:title &>
</%method>
