<%inherit file="/base.mako" />
<h2>Closed!</h2>

<p>
<p>Editing has been disabled while proposals are reviewed. If your proposal is successful in its submission, you will be able to update your details later when the schedule is finalised.</p>
</p>

<p>
Return to the <a href="${ h.url_for("home") }">main page</a>.
</p>

<%def name="title()">
Submission Editing - closed - ${ parent.title() }
</%def>
