<%inherit file="/base.mako" />

<h2 class="pop">Edit payment</h2>

<p>Use this form to process a manual payment, such as one received by direct
credit or cheque.</p>

${ h.form(h.url_for()) }

<%include file="form.mako" args="editing=True" />

<p class="submit">${ h.submit("Update", "Update payment",) }</p>

${ h.end_form() }


