<%inherit file="/base.mako" />
    <div id="actions">
      <ul>
        <li>${ h.link_to('Registration status', url=h.url_for(controller='registration', action='status')) }</li>
        <li>${ h.link_to('Printable version', url=h.url_for(action='printable')) }</li>
        <li>${ h.link_to('PDF version', url=h.url_for(action='pdf')) }</li>
% if not c.invoice.is_void() and c.invoice.paid():
        <li>Invoice has been paid.</li>
% elif c.invoice.bad_payments:
        <li>Invalid payments have been applied to this invoice, please email ${ h.contact_email('the organising committee') }</a></li>
% elif not c.invoice.is_void() and not c.invoice.paid():
        <li>${ h.link_to('Pay this invoice', url = h.url_for(action='pay')) }</li>
        <li>
          ${ h.link_to('Regenerate invoice', url = h.url_for(controller='registration', action='pay', id=c.invoice.person.registration.id)) }
          <br><span style="font-size: small;">Use the regenerate invoice link if you have edited your registration but the invoice doesn't look quite right.</span>
        </li>
% endif
      </ul>
%   if 'invoice_message' in h.lca_info and (c.invoice.is_void() or not c.invoice.paid()):
          <p><small><strong>Please Note:</strong> ${ h.lca_info['invoice_message'] }</small></p>
%   endif
    </div>

<%include file="view_fragment.mako" />

<%def name="title()">
Tax Invoice/Statement - ${ caller.title() }
</%def>
