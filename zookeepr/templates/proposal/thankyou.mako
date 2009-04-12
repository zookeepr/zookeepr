<%inherit file="/base.mako" />

<h2>Call for Presentations</h2>

<h3>Thank You</h3>

<p>
Thank you for your presentation submission.
</p>

<p>
<a href="${ h.url_for(action="new", id=None) }">Submit another presentation</a>,
<a href="${ h.url_for(action="index", id=None) }">edit your submissions</a> or
return to the <a href="${ h.url_for("home") }">main page</a>.
</p>
