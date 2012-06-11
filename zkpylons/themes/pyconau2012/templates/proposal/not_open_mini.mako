<%inherit file="/base.mako" />
<h2>Nice Try!</h2>

<p>
Yes PyCon Australia are using <a href="http://zkpylons.org">zkpylons</a> which was built for <a href="http://linux.conf.au">linux.conf.au</a> and yes there is a lot of bad code left over, but we did tie up some loose ends. Sorry to disappoint but we won't be having miniconfs at PyCon Australia.
</p>

<p>
Return to the <a href="${ h.url_for("home") }">main page</a>.
</p>

<%def name="title()">
Call for Miniconfs - coming soon - ${ parent.title() }
</%def>
