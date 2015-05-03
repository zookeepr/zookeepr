<%inherit file="/base.mako" />

<h2>${ c.config.get('event_name') } Funding Application</h2>
<p>Please read the <a href="${ h.url_for("/register/funding") }">Funding Info</a> page before submitting a funding application.</p>

${ h.form(h.url_for(), multipart=True) }
<%include file="form.mako" args="editing=False" />

  <p class="submit">${ h.submit('submit', 'Submit!') }</p>
${ h.end_form() }

<%def name="short_title()"><%
  return "Submit a Funding Request"
%></%def>
<%def name="title()" >
Submit a Funding Request - ${ parent.title() }
</%def>
