<%inherit file="/base.mako" />
<%
    c.form = 'new_incomplete'
%>
<h2 class="pop">Creation of a new incomplete user account</h2>

<p>This form allows organizers to manually create incomplete accounts for other people.</p>

<p>These accounts can be assigned roles or edited but they will not have a password associated with them. The ownwer of that email address will have to use Persona to log in or request a password reset via email.</p>

${ h.form(h.url_for(), method='post') }

<p class="label"><span class="mandatory">*</span><label for="person.email_address">Email address:</label></p>
<p class="entries">${ h.text('person.email_address', size=40) }</p>

<p class="submit">${ h.submit("submit", "Create a new account",) }</p>

${ h.end_form() }
