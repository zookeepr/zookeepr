<%inherit file="/base.mako" />
<%
    c.form = 'new_manual'
%>
<h2 class="pop">New payment</h2>

<p>Use this form to process a manual payment, such as one received by direct
credit or cheque.</p>

${ h.form(h.url_for(), method='post') }

<%include file="form.mako" />

<p class="submit">${ h.submit("submit", "Create a new payment",) }</p>

${ h.end_form() }


