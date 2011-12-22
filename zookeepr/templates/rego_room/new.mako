<%inherit file="/base.mako" />

<h2>Add a new room</h2>
${ h.form(h.url_for(action='new')) }
<%include file="form.mako" />
<p>${ h.submit('submit', 'Save') }
% if c.rego_id:
${ h.link_to('Back', url=h.url_for(controller='registration', action='index')) }
% else:
${ h.link_to('Back', url=h.url_for(action='index')) }
% endif
</p>
${ h.end_form() }

<%def name="title()">
New room - ${ parent.title() }
</%def>
