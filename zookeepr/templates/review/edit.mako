<%inherit file="/base.mako" />
<%namespace file="../proposal/reviewer_sidebar.mako" name="sidebar" inheritable="True"/>
<%def name="toolbox_extra()">
  ${ parent.toolbox_extra() }
  ${ self.sidebar.toolbox_extra() }
</%def>

<h1>Review update</h1>

<p>You may modify your review with this form. The original proposal is below.</p>

<div id="review">
${ h.form(h.url_for()) }
<%include file="form.mako" />
<p>${ h.submit('update', 'Update') }</p>
${ h.end_form() }
</div>

<%def name="title()" >
Review of <% h.truncate(c.review.proposal.title) %> - ${ parent.title() }
</%def>

