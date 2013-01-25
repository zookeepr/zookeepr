<%inherit file="/base.mako" />

<h1>Funding Application Review Update</h1>

<p>You may modify your review with this form. The original funding application is below.</p>

<hr>
<%include file="/funding/view_fragment.mako" />

<div id="review">
${ h.form(h.url_for()) }
<%include file="form.mako" />
<p>${ h.submit('update', 'Update') } or ${ h.link_to('Go Back', url=h.url_for(action='view', id=c.review.id)) }</p>
${ h.end_form() }
</div>

<%def name="title()" >
Review of <% c.funding.person.fullname %>'s <% h.truncate(c.funding.type.name) %> - ${ parent.title() }
</%def>

