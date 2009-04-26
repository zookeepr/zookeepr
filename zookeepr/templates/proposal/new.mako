<%inherit file="/base.mako" />

<h2>Propose a talk or tutorial</h2>
<p>Please read the <a href="${ h.url_for("/programme/presenter_faq") }">Presenter FAQ</a> before submitting a proposal.</p>

${ h.form(h.url_for(), multipart=True) }
<%include file="form.mako" />

  <p class="submit">${ h.submit('submit', 'Submit!') }</p>
${ h.end_form() }

<%def name="title()" >
Call for Presentations - ${ caller.title() }
</%def>
