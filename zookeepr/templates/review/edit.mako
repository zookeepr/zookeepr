<%inherit file="/base.mako" />

<h1>Review update</h1>

<p>You may modify your review with this form. The original proposal is below.</p>

<div class="contents"><h3>Review Pages</h3>
<ul>
<%include file="../proposal/reviewer_sidebar.mako" />
</ul>
</div>

<div id="review">
${ h.form(h.url_for()) }
<%include file="form.mako" />
<p>${ h.submit('update', 'Update') }</p>
${ h.end_form() }
</div>

<%def name="title()" >
Review of <% h.truncate(c.review.proposal.title) %> - ${ caller.title() }
</%def>

