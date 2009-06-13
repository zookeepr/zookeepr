<%inherit file="/base.mako" />

<h2>Propose a Miniconf</h2>
<p>Please read the Miniconf organiser section in the <a href="${ h.url_for("/programme/presenter_faq") }">Presenter FAQ</a> before submitting a proposal.</p>

${ h.form(h.url_for(), multipart=True) }
<%include file="form_mini.mako" />

  <p class="submit">${ h.submit('submit', 'Submit!') }</p>
${ h.end_form() }

<%def name="title()" >
Submit a Miniconf - ${ parent.title() }
</%def>

