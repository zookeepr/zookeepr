<%inherit file="/base.mako" />

<h2>Coming soon!</h2>

<p>
The funding requests has not opened yet. This means you can't edit any
requests yet! lease visit back later.
</p>

<p>
Return to the <a href="${ h.url_for("home") }">main page</a>.
</p>

<%def name="title()" >
Editing Funding Request - coming soon - ${ parent.title() }
</%def>
