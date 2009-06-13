<%inherit file="/base.mako" />

<h2>Propose a Presentation or Tutorial</h2>
<p>Please read the <a href="${ h.url_for("/programme/presenter_faq") }">Presenter FAQ</a> before submitting a paper.</p>

${ h.form(h.url_for(), multipart=True) }
<%include file="form.mako" />

  <p class="submit">${ h.submit('submit', 'Submit!') }</p>
${ h.end_form() }

<%def name="title()" >
Submit a Presentation - ${ parent.title() }
</%def>
