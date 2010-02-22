<%inherit file="/base.mako" />
<h2>Edit Funding Request</h2>

<div id="funding_request">

${ h.form(h.url_for()) }

<%include file="form.mako" args="editing=True" />

<p class="submit">
${ h.submit('Update', 'Update') }
</p>

${ h.end_form() }

</div>

