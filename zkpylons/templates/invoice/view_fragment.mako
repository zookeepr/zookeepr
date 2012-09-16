    <h1>Tax Invoice/Statement</h1>

% if c.invoice.is_void:
<%   invalid = " invoice_invalid" %>
% else:
<%   invalid = "" %>
% endif
<div class="invoice${ invalid }">
    <div style="text-align:center">
      <h2>${ h.lca_info['event_parent_organisation'] }</h2>
      <p>${ h.lca_info['event_tax_number'] }</p>
    </div>
    <p><strong>Invoice Number:</strong> ${ c.invoice.id }</p>
    <p><strong>Invoice Status:</strong> ${ c.invoice.status }
% if c.invoice.is_void:
<span style="font-size: 22px; color: #F00"> - ${ c.invoice.void }</span>
% endif
    </p>
    <p><strong>Issue Date:</strong> ${ c.invoice.issue_date.strftime("%d %b %Y") }</p>
    <p><strong>Due Date:</strong> ${ c.invoice.due_date.strftime("%d %b %Y") }</p>
% if c.invoice.is_paid:
    <p><strong>Invoice Paid</strong></p>
% elif c.invoice.total == 0:
    <p><strong>No Payment Required</strong></p>
% else:
    <p><strong>Amount Due:</strong> ${ h.integer_to_currency(c.invoice.total) }</p>
% endif

    <p>
      <strong>Attention:</strong> ${ c.invoice.person.firstname } ${ c.invoice.person.lastname }
% if c.invoice.person.registration and c.invoice.person.company:
      <br><strong>Company:</strong> ${ c.invoice.person.company }
% endif
    </p>

    <p><strong>Regarding:</strong> ${ h.event_name() }</p>

    <p>This invoice has been issued as a result of an application to attend ${ h.event_name() }.</p>

    <table style="width: 100%">
      <thead><tr>
        <th>Description</th>
        <th>Qty</th>
        <th>Cost</th>
        <th>Total (Inc. GST)</th>
      </tr></thead>
% for item in c.invoice.items:
%   if not (item.cost == 0 and item.product and item.product.category.invoice_free_products == False):
      <tr class="${ h.cycle('even', 'odd') }">
        <td>${ item.description }</td>
        <td style="text-align:center">${ item.qty }</td>
        <td style="text-align:right">${ h.integer_to_currency(item.cost) }</td>
        <td style="text-align:right">${ h.integer_to_currency(item.total) }</td>
      </tr>
%   endif
% endfor
      <tr>
        <td style="text-align: right" colspan="3"><strong>Total</strong></td>
        <td style="text-align: right"><strong>${ h.integer_to_currency(c.invoice.total) }</strong></td>
      </tr>
      <tr>
        <td style="text-align: right" colspan="3">(Includes AU GST</td>
        <td style="text-align: right">${ h.integer_to_currency(h.sales_tax(c.invoice.total)) })</td>
      </tr>
    </table>
% if c.invoice.is_void:
%   if c.invoice.person.registration:
        <p class="pay_button">This invoice has been cancelled. You must now ${ h.link_to('generate a new invoice', url=h.url_for(controller='registration', action='pay', id=c.invoice.person.registration.id)) }</p>
%   endif
% elif c.invoice.is_paid:
        <p class="pay_button">Invoice has been <b>paid</b>.
%   if c.invoice.total > 0:
Receipt number: <code>PR${ c.payment_received.id }P${ c.payment.id }</code>
%   endif
</p>
% elif len(c.invoice.bad_payments) > 0:
        <p class="pay_button">Invalid payments have been applied to this invoice, please ${ h.link_to('try again', url=h.url_for(action='void', id=c.invoice.id)) } or email ${ h.contact_email('the organising committee') }</a></p>
% else:
        <p class="pay_button">${ h.link_to('Pay this invoice', url = h.url_for(action='pay')) }</p>
% endif
% if c.invoice.person.registration:
    <p>Further information on your registration is available at: ${ h.link_to(h.url_for(qualified=True, controller='registration', action='status', id=c.invoice.person.registration.id), h.url_for(qualified=True, controller='registration', action='status', id=c.invoice.person.registration.id)) }</p>
% endif
    <p>
      Enquiries may be emailed to the organisers:
% if c.printable:
      ${ h.contact_email() }.
% else:
      ${ h.contact_email('contact email') }.
% endif
    </p>

    <div style="text-align:center">
      <p>${ h.link_to(h.lca_info['event_name'], url=h.lca_info['event_url']) } is a project of ${ h.link_to(h.lca_info['event_parent_organisation'], url=h.lca_info['event_parent_url']) }.</p>
      <p>
        ${ h.lca_info['event_postal_address'] }<br>
        ${ h.lca_info['event_tax_number'] }<br>
        Phone: ${ h.lca_info['event_phone_number'] }<br>
        Fax: ${ h.lca_info['event_fax_number'] }<br>
      </p>
    </div>
</div>
