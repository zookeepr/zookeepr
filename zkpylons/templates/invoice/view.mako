<%inherit file="/base.mako" />
    <div id="actions">
      <ul>
% if h.auth.authorized(h.auth.has_organiser_role):
        <li>${ h.link_to(c.invoice.person.firstname + "'s Profile", url=h.url_for(controller='person', action='view', id=c.invoice.person.id)) }</li>
% endif
% if c.invoice.person.registration is not None:
        <li>${ h.link_to('Registration status', url=h.url_for(controller='registration', action='status', id=c.invoice.person.registration.id)) }</li>
% endif
        <li>${ h.link_to('Printable version', url=h.url_for(action='printable')) }</li>
        <li>${ h.link_to('PDF version', url=h.url_for(action='pdf')) }</li>
        <li>${ h.link_to('Generate access URL', url=h.url_for(action='generate_hash')) }</li>
% if h.auth.authorized(h.auth.has_organiser_role):
%   if c.invoice.is_void:
        <li>${ h.link_to('Unvoid this invoice', url = h.url_for(action='unvoid')) }</li>
         <ul><li>Unvoiding invoices marks them as manual.</li></ul>
%   else:
        <li>${ h.link_to('Void this invoice', url = h.url_for(action='void')) }</li>
%   endif
% endif
% if c.invoice.is_void and c.invoice.person.registration:
%   if h.auth.authorized(h.auth.has_organiser_role):
        <li>${  h.link_to('Generate a new invoice', url=h.url_for(controller='registration', action='pay', id=c.invoice.person.registration.id)) }</li>
%   else:
        <li>This invoice has been cancelled. You must now ${ h.link_to('generate a new invoice', url=h.url_for(controller='registration', action='pay', id=c.invoice.person.registration.id)) }</li>
%   endif
% elif c.invoice.is_paid:
%   if h.auth.authorized(h.auth.has_organiser_role):
        <li>Invoice was paid by ${ c.invoice.person.email_address }.</li>
%   else:
        <li>Invoice has been paid.</li>
%   endif
% elif len(c.invoice.bad_payments) > 0:
        <li>Invalid payments have been applied to this invoice, please ${ h.link_to('try again', url=h.url_for(action='void', id=c.invoice.id)) } or email ${ h.contact_email('the organising committee') }</a></li>
% else:
%   if h.auth.authorized(h.auth.has_organiser_role):
        <li>${ h.link_to('Pay this invoice manually', url = h.url_for(action='pay_manual')) }</li>
         <ul><li>Use this if the person has paid via direct credit to the bank account or similar</li></ul>
%   endif
        <li>${ h.link_to('Pay this invoice', url = h.url_for(action='pay')) }</li>
%   if c.invoice.person.registration:
        <li>${ h.link_to('Regenerate invoice', url = h.url_for(controller='registration', action='pay', id=c.invoice.person.registration.id)) }</li>
        <ul>
          <li><span style="note">Use the regenerate invoice link if you have edited your registration but the invoice doesn't look quite right.</li>
        </ul>
%   endif
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
              Payment Received ${ h.link_to(str(pr.id), url=h.url_for(controller='payment', action='view', id=pr.payment.id)) } (${ pr.email_address })
%       if pr.validation_errors:
              -- <font color="red">Validation errors</font>
%       endif
            </li>
%     endfor
%     for payment in c.invoice.payments:
            <li>
              Payment ${ h.link_to(str(payment.id), url=h.url_for(controller='payment', action='view', id=payment.id)) } (${ payment.invoice.person.email_address })
%       if not payment.invoice.is_paid:
              ${ h.link_to("Add Payment", url=h.url_for(controller='payment', action='new_manual', id=payment.id)) }
%       endif
            </li>
%     endfor
        </ul>
%endif
      </ul>
%   if 'invoice_message' in h.lca_info and (c.invoice.is_void or not c.invoice.is_paid):
          <p style="note"><strong>Please Note:</strong> ${ h.lca_info['invoice_message'] }</p>
%   endif
    </div>

<%include file="view_fragment.mako" />

<%def name="title()">
Tax Invoice/Statement - ${ parent.title() }
</%def>
