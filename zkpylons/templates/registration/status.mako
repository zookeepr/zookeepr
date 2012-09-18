<%inherit file="/base.mako" />

<%
"""
    <div class="notice-box">
% if h.lca_info['conference_status'] == 'not_open':
      <b>Registrations</b> are <i>not</i> open<br><br>
% elif h.lca_info['conference_status'] == 'open' and c.ceilings['conference-paid'].available():
      <b>Registrations</b> are open<br><br>
% else:
      <b>Registrations are closed</b><br><br>
% endif
    </div>
"""
%>
      <h3>Conference Status</h3>
% if h.lca_info['conference_status'] == 'open' and c.ceilings['conference-earlybird'].available() and c.ceilings['conference-paid'].available():
      <b>Earlybird</b> registrations are currently available! Only a limited number of Earlybird registrations are available however so be sure to pay before they're all gone.<br />
      Earlybird sales status:<br />
      
      <div class="graph-bar-sold" style = "width:${ h.number_to_percentage(c.ceilings['conference-earlybird'].percent_invoiced())}; text-align:center">
% if c.ceilings['conference-earlybird'].percent_invoiced() > 10: #Only display the Sold text if there is enough room
      Sold (${ h.number_to_percentage(c.ceilings['conference-earlybird'].percent_invoiced()) })
% endif
      </div>
      <div class="graph-bar-available" style = "width:${ h.number_to_percentage(100-c.ceilings['conference-earlybird'].percent_invoiced()) }; text-align:center">
% if c.ceilings['conference-earlybird'].percent_invoiced() < 85: #Only display the Available text if there is room
      Available 
% endif
      (${ h.number_to_percentage(100-c.ceilings['conference-earlybird'].percent_invoiced()) })
      </div>

% elif h.lca_info['conference_status'] == 'open' and c.ceilings['conference-paid'].available() and not c.ceilings['conference-earlybird'].available():
      
      <div class="graph-bar-sold" style = "width:${ h.number_to_percentage(c.ceilings['conference-paid'].percent_invoiced())}; text-align:center">
% if c.ceilings['conference-paid'].percent_invoiced() > 10: #Only display the Sold text if there is enough room
      Sold (${ h.number_to_percentage(c.ceilings['conference-paid'].percent_invoiced()) })
% endif
      </div>

     <div class="graph-bar-available" style = "width:${ h.number_to_percentage(100-c.ceilings['conference-paid'].percent_invoiced()) }; text-align:center">
% if c.ceilings['conference-paid'].percent_invoiced() < 85: #Only display the Available text if there is room
      Available
% endif
% if c.ceilings['conference-paid'].percent_invoiced() < 95: #Only display the Available text if there is room
      (${ h.number_to_percentage(100-c.ceilings['conference-paid'].percent_invoiced()) })
% endif
      </div>


% endif

% if 'conference-paid' not in c.ceilings or (c.registration is None and h.lca_info['conference_status'] == 'not_open'):
    <h2>Registrations are not open</h2>
    <p>Registrations are not yet open. Please come back soon!</p>
% elif c.registration is None and h.lca_info['conference_status'] == 'closed':
    <h2>Registrations are closed</h2>
    <p>Registrations are completely closed.</p>
% else:

% if not c.ceilings['conference-paid'].available():
    <h2>Registrations are closed</h2>
    <p>Registrations are now closed. You will only be able to register if you
    have an existing voucher code or if you're otherwise entitled to attend
    for free (eg speakers).</p>
% endif
    <br />
    <h3>Your registration status</h3>

% if c.registration is None:
    <p><b>Not registered.</b>

<%include file="volunteer.mako" />

    <h3>Next step</h3>

    <p>${ h.link_to('Fill in registration form', h.url_for(action='new')) }.</p>

% elif c.registration:
%   if c.person.paid():
    <p><b>Registered and paid.</b></p>
%   else:
    <p><b>Tentatively registered.</b></p>
%   endif

    <%include file="volunteer.mako" />

%   if not c.person.paid():
    <h3>Next steps</h3>

%       if c.person.valid_invoice():
%           if c.manual_invoice(c.person.invoices):
    <p>Please see the invoices listed below</p>
%           elif c.person.paid():
    <p>${ h.link_to('View Invoice', h.url_for(controller='invoice', action='view', id=c.person.valid_invoice().id)) }</p>
%           else:
    <p>${ h.link_to('Pay Invoice', h.url_for(action='pay', id=c.registration.id)) }</p>
%           endif
%       else:
%           if c.manual_invoice(c.person.invoices):
    <p>Please see the invoices listed below</p>
%           else:
    <p>${ h.link_to('Generate Invoice', h.url_for(action='pay', id=c.registration.id)) }</p>
%           endif
%       endif
%   endif

    <h3>Other options</h3>

    <p>
%   if c.person.volunteer and (c.person.volunteer.accepted or c.person.volunteer.accepted is None):
    ${ h.link_to('Change volunteer areas of interest', h.url_for(controller='volunteer', action='edit', id=c.person.volunteer.id)) }<br>
%   endif
    ${ h.link_to('Edit details', h.url_for(action='edit', id=c.registration.id)) }<br>
%   if c.person.valid_invoice() and c.person.valid_invoice().is_paid:
    ${ h.link_to('View invoice', h.url_for(controller='invoice', action='view', id=c.person.valid_invoice().id)) }<br>
%   else:
    ${ h.link_to('Pay invoice', h.url_for(action='pay', id=c.registration.id)) }<br>
%   endif
    ${ h.link_to('View details', h.url_for(action='view', id=c.registration.id)) }<br>
    <table>
      <tr>
        <th>Invoice #</th>
        <th>Status</th>
        <th>Amount</th>
        <th></th>
      </tr>
%   for invoice in c.person.invoices:
      <tr>
        <td>${ h.link_to(invoice.id, h.url_for(controller='invoice', action='view', id=invoice.id)) }</td>
        <td>${ invoice.status }</td>
        <td>${ h.number_to_currency(invoice.total / 100) }</td>
        <td>
          ${ h.link_to('View', h.url_for(controller='invoice', action='view', id=invoice.id)) } - Print
          ${ h.link_to('html', h.url_for(controller='invoice', action='printable', id=invoice.id)) },
          ${ h.link_to('pdf', h.url_for(controller='invoice', action='pdf', id=invoice.id)) }
        </td>
      </tr>
%   endfor
    </table>

% elif False and c.person.invoices[0].bad_payments.count() > 0:
    <p><b>Tentatively registered and tried to pay.</b></p>

    <p>Unfortunately, there was some sort of problem with your payment.</p>

    <h3>Next step</h3>

    <p>${ h.contact_email("Contact the committee") }</p>

    <p>Your details are:
    person ${ c.person.id },
    registration ${ c.registration.id },
    invoice ${ c.person.invoices[0].id }.</p>

    <h3>Other option</h3>
    ${ h.link_to("View registration details", url=h.url_for(action="view", id=c.registration.id)) }<br>

% else:
    <p>Interesting!</p>
% endif

    <h3>Summary of steps</h3>
% if c.person:
    <p>${ h.yesno(c.registration != None) |n} Fill in registration form
    <br>${ h.yesno(c.person.valid_invoice()) |n} Generate invoice
    <br>${ h.yesno(c.person.paid()) |n} Pay
    <br>${ h.yesno(False) |n} Attend conference</p>
% else:
    <p>${ h.yesno(False) |n} Fill in registration form
    <br>${ h.yesno(False) |n} Generate invoice
    <br>${ h.yesno(False) |n} Pay
    <br>${ h.yesno(False) |n} Attend conference</p>
% endif
% endif

<%def name="title()" >
Registration Status - ${ c.person.fullname() } - ${ parent.title() }
</%def>

