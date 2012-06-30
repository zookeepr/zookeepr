<%inherit file="/base.mako" />

<h2>Coming soon!</h2>

<p>
The call for proposals has not opened yet. Please visit back later.
</p>

<p>
Return to the <a href="${ h.url_for("home") }">main page</a>.
</p>

<%def name="title()" >
Call for Papers - coming soon - ${ parent.title() }
</%def>
