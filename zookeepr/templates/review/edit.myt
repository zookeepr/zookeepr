<&| @zookeepr.lib.form:fill, defaults=defaults, errors=errors &>
<h1>Review update</h1>

<p>You may modify your review with this form. The original proposal is below.</p>

<div class="contents"><h3>Review Pages</h3>
<ul>
<& ../proposal/reviewer_sidebar.myt &>
</ul>
</div>

<div id="review">
<% h.form(h.url()) %>
<& form.myt &>
<p><% h.submitbutton('Update') %></p>
<% h.end_form() %>
</div>

<& ../proposal/view.myt &>

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
        'review.miniconf': c.review.miniconf,
        'review.stream': c.review.stream.id
        }
</%init>

<%method title>
Review of <% h.truncate(c.review.proposal.title) %> - <& PARENT:title &>
</%method>
