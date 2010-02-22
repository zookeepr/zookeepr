<%inherit file="/base.mako" />
<h2>Closed!</h2>

<p>
Editing has been disabled while funding requests are reviewed.
</p>

<p>
Return to the <a href="${ h.url_for("home") }">main page</a>.
</p>

<%def name="title()">
Funding Editing - closed - ${ parent.title() }
</%def>
