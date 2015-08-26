<%inherit file="/base.mako" />
<h2>Oops!</h2>

<p>
The page you requested does not actually exist.
</p>

<p>
We admire your enthusiasm for requesting information, but this page simply does not exist. If you think that's wrong, you can ${ h.email_link_to(c.config.get('webmaster_email'), "send us an email") } and we'll attend to the problem.
</p>

<%def name="title()">
Page not found! -
 ${ parent.title() }
</%def>
