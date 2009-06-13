<%inherit file="/base.mako" />

<h2>Withdraw this proposal</h2>

${ h.form(h.url_for()) }

<p>Are you sure you want to withdraw this proposal?</p>

<p>If you withdraw a proposal, it will <b>no longer be considered for acceptance</b>.</p>

<p>${ h.submit('submit', 'Yes, withdraw') }
or ${ h.link_to('No, take me back.', url=h.url_for(controller='proposal', action='index')) }</p>

${ h.end_form() }
