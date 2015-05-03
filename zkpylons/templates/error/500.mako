<%inherit file="/base.mako" />
<h2>Oops!</h2>

<p>
There was an unexpected error.
</p>

<p>
If you think that's a problem, you can ${ h.email_link_to(c.config.get('webmaster_email'), "send us an email") } and we'll attend to the problem.
</p>

<%def name="title()">
Unexpected Error! -
 ${ parent.title() }
</%def>
