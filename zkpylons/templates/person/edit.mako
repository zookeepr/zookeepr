<%inherit file="/base.mako" />
<h2>Edit person</h2>

<p class="label">If you need to change your password you may use the ${ h.link_to("Forgotten Password Service", url=h.url_for(controller='person', action='forgotten_password')) }. We would like to avoid the changing of email addresses, however if you require your account email address to be updated, please contact ${ h.email_link_to(c.config.get('webmaster_email')) }.</p>

${ h.form(h.url_for(id=c.person.id)) }

<%include file="form.mako" />

<p>${ h.submit('update', 'Update') }</p>

${ h.end_form() }

