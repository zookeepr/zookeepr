<%inherit file="/base.mako" />

<h2>Coming soon!</h2>

<p>
Funding requests can not be submitted yet. Please visit back later.
</p>

<p>
Return to the <a href="${ h.url_for("home") }">main page</a>.
</p>

<%def name="title()" >
Funding Requests - coming soon - ${ parent.title() }
</%def>
