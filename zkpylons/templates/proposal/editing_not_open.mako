<%inherit file="/base.mako" />

<h2>Coming soon!</h2>

<p>
The call for proposals has not opened yet. This means you can't edit any
proposals yet! lease visit back later.
</p>

<p>
Return to the <a href="${ h.url_for("home") }">main page</a>.
</p>

<%def name="title()" >
Editing Submissions - coming soon - ${ parent.title() }
</%def>
