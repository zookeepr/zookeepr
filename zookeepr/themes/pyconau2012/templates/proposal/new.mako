<%inherit file="/base.mako" />

<h2>Submit a Proposal</h2>
<p>Please read the <a href="${ h.url_for("/programme/call_for_proposals") }">Call for Proposals</a> page before submitting a proposal.</p>

${ h.form(h.url_for(), multipart=True) }
<%include file="form.mako" args="editing=False" />

  <p class="submit">${ h.submit('submit', 'Submit!') }</p>
${ h.end_form() }

<%def name="short_title()"><%
  return "Submit a Proposal"
%></%def>
<%def name="title()" >
Submit a Proposal - ${ parent.title() }
</%def>
