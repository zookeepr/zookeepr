<%inherit file="/base.mako" />
<h2>Closed!</h2>

<p>
Editing of submissions is now closed!
</p>

<p>
Return to the <a href="${ h.url_for("home") }">main page</a>.
</p>

<%def name="title()">
Submission Editing - closed - ${ parent.title() }
</%def>
