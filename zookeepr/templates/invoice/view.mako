<%inherit file="/base.mako" />
    <div id="actions">
      <ul>
        <li>${ h.link_to('Registration status', url=h.url_for(controller='registration', action='status')) }</li>
        <li>${ h.link_to('Printable version', url=h.url_for(action='printable')) }</li>
        <li>${ h.link_to('PDF version', url=h.url_for(action='pdf')) }</li>
% if not c.invoice.is_void() and c.invoice.paid():
%   if h.auth.authorized(h.auth.has_organiser_role):
        <li>Invoice was paid by ${ c.invoice.person.email_address }.</li>
%   else:
        <li>Invoice has been paid.</li>
%   endif
% elif c.invoice.bad_payments().count() > 0:
        <li>Invalid payments have been applied to this invoice, please email ${ h.contact_email('the organising committee') }</a></li>
% elif not c.invoice.is_void() and not c.invoice.paid():
        <li>${ h.link_to('Pay this invoice', url = h.url_for(action='pay')) }</li>
        <li>
          ${ h.link_to('Regenerate invoice', url = h.url_for(controller='registration', action='pay', id=c.invoice.person.registration.id)) }
          <br><span style="font-size: small;">Use the regenerate invoice link if you have edited your registration but the invoice doesn't look quite right.</span>
        </li>
% endif

%if h.auth.authorized(h.auth.has_organiser_role):
        <ul>
%     for pr in c.invoice.payment_received:
            <li>
%       if pr.approved:
              <font color="green">APPROVED</font>
%       else:
              <font color="red">DECLINED</font>
%       endif
              PaymentReceived ${ h.link_to(str(pr.id), url=h.url_for(controller='payment', action='view', id=pr.payment.id)) } (${ pr.email_address })
%       if pr.validation_errors:
              -- <font color="red">Validation errors</font>
%       endif
            </li>
%     endfor
%     for payment in c.invoice.payments:
            <li>Payment ${ h.link_to(str(payment.id), url=h.url_for(controller='payment', action='view', id=payment.id)) } (${ payment.invoice.person.email_address })</li>
%     endfor
        </ul>
%endif
      </ul>
%   if 'invoice_message' in h.lca_info and (c.invoice.is_void() or not c.invoice.paid()):
          <p><small><strong>Please Note:</strong> ${ h.lca_info['invoice_message'] }</small></p>
%   endif
    </div>

<%include file="view_fragment.mako" />

<%def name="title()">
Tax Invoice/Statement - ${ parent.title() }
</%def>
