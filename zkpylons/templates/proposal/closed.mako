<%inherit file="/base.mako" />
<h2>Closed!</h2>

<p>
The call for proposals is now closed!
</p>

<p>
Return to the <a href="${ h.url_for("home") }">main page</a>.
</p>

<%def name="title()">
Call for Papers - closed - ${ parent.title() }
</%def>
