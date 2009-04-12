<%inherit file="/base.mako" />

<h2>Edit Volunteer</h2>
% if h.signed_in_person() != c.volunteer.person:
    <p class="error-message">You're looking at (and editing) ${ c.volunteer.person.firstname |h} ${ c.volunteer.person.lastname |h}'s info, not your own!</p>
% endif

${ h.form(h.url_for(id=c.volunteer.id)) }
<%include file="form.mako" />
<p>${ h.submit('submit', 'Update') }</p>
${ h.end_form() }
