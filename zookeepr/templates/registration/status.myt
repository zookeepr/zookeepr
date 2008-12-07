    <div class="notice-box">
% if h.lca_info['conference_status'] == 'not_open':
      <b>Registrations</b> are <i>not</i> open<br><br>
% elif h.lca_info['conference_status'] == 'open' and c.ceilings['conference'].available():
      <b>Registrations</b> are open<br><br>
% else:
      <b>Registrations are closed</b><br><br>
% #endif
      <div class = "graph-bar" style = "width:<% h.number_to_percentage(c.ceilings['conference'].percent_invoiced(), precision=0) %>">&nbsp;</div>
      <div class = "graph-bar-text"><% h.ticket_percentage_text(c.ceilings['conference'].percent_invoiced()) %></div><br>
% if h.lca_info['conference_status'] == 'open' and c.ceilings['earlybird'].available() and c.ceilings['conference'].available():
      <b>Earlybird</b> is available<br><br>
      <div class = "graph-bar" style = "width:<% h.number_to_percentage(c.ceilings['earlybird'].percent_invoiced(), precision=0) %>">&nbsp;</div>
      <div class = "graph-bar-text"><% h.ticket_percentage_text(c.ceilings['earlybird'].percent_invoiced(), True) |h%></div><br>
% else:
      <b>Earlybird not available</b><br><br><% c.ebtext |h%>
% #endif
      <b><%c.timeleft %></b>
    </div>

% if h.lca_info['conference_status'] == 'not_open':
    <h2>Registrations are not open</h2>
    <p>Registrations are not yet open. Please come back soon!</p>
% elif h.lca_info['conference_status'] == 'closed':
    <h2>Registrations are closed</h2>
    <p>Registrations are completely closed.</p>
% else:

% if not c.ceilings['conference'].available():
    <h2>Registrations are closed</h2>
    <p>Registrations are now closed. You will only be able to register if you
    have an existing voucher code or if you're otherwise entitled to attend
    for free (eg speakers).</p>
% #endif
    <h3>Your registration status</h3>

% if not c.signed_in_person:
    <p><b>Not signed in.</b></p>

    <h3>Next step</h3>

    <p><% h.link_to('Sign in', h.url(controller='person', action='signin')) %> if you already have an account
    (you've already registered, submitted a proposal or similar).  If you can't log in, you can try
    <% h.link_to('recovering your password', h.url(controller='person', action='forgotten_password')) %>.</p>
%   session['sign_in_redirect'] = h.url_for(action='status')
%   session.save()

    <p><b><% h.link_to('Go directly to the registration form', h.url(action='new')) %> otherwise.</b></p>

% elif c.signed_in_person and c.signed_in_person.registration == None:
    <p><b>Not registered.</b>

    <& volunteer.myt &>

    <h3>Next step</h3>

    <p><% h.link_to('Fill in registration form', h.url(action='new')) %>.</p>

% elif c.signed_in_person and c.signed_in_person.registration:
%   if c.signed_in_person.paid():
    <p><b>Registered and paid.</b></p>
%   else:
    <p><b>Tentatively registered.</b></p>
%   #endif

<& volunteer.myt &>

%   if not c.signed_in_person.paid():
    <h3>Next step</h3>

%       if c.signed_in_person.valid_invoice():
%           if c.manual_invoice(c.signed_in_person.invoices):
    <p>Please see the invoices listed below</p>
%           elif c.signed_in_person.paid():
    <p><% h.link_to('View Invoice', h.url(controller='invoice', action='view', id=c.signed_in_person.valid_invoice().id)) %></p>
%           else:
    <p><% h.link_to('Pay Invoice', h.url(action='pay', id=c.signed_in_person.registration.id)) %></p>
%           #endif
%       else:
%           if c.manual_invoice(c.signed_in_person.invoices):
    <p>Please see the invoices listed below</p>
%           else:
    <p><% h.link_to('Generate Invoice', h.url(action='pay', id=c.signed_in_person.registration.id)) %></p>
%           #endif
%       #endif
%   #endif

    <h3>Other options</h3>

    <p>
%   if c.signed_in_person.volunteer and (c.signed_in_person.volunteer.accepted or c.signed_in_person.volunteer.accepted is None):
    <% h.link_to('Change volunteer areas of interest', h.url(controller='volunteer', action='edit', id=c.signed_in_person.volunteer.id)) %><br>
%   #endif
    <% h.link_to('Edit details', h.url(action='edit', id=c.signed_in_person.registration.id)) %><br>
%   if c.signed_in_person.valid_invoice() and c.signed_in_person.valid_invoice().paid():
    <% h.link_to('View invoice', h.url(controller='invoice', action='view', id=c.signed_in_person.valid_invoice().id)) %><br>
%   else:
    <% h.link_to('Pay invoice', h.url(action='pay', id=c.signed_in_person.registration.id)) %><br>
%   #endif
    <% h.link_to('View details', h.url(action='view', id=c.signed_in_person.registration.id)) %><br>
    <table>
      <tr>
        <th>Invoice #</th>
        <th>Status</th>
        <th>Amount</th>
        <th></th>
      </tr>
%   for invoice in c.signed_in_person.invoices:
      <tr>
        <td><% h.link_to(invoice.id, h.url(controller='invoice', action='view', id=invoice.id)) %></td>
        <td><% invoice.status() %></td>
        <td><% h.number_to_currency(invoice.total() / 100) %></td>
        <td>
          <% h.link_to('View', h.url(controller='invoice', action='view', id=invoice.id)) %> - Print
          <% h.link_to('html', h.url(controller='invoice', action='printable', id=invoice.id)) %>,
          <% h.link_to('pdf', h.url(controller='invoice', action='pdf', id=invoice.id)) %>
        </td>
      </tr>
%   #endfor
    </table>

% elif False and c.signed_in_person.invoices[0].bad_payments:
    <p><b>Tentatively registered and tried to pay.</b></p>

    <p>Unfortunately, there was some sort of problem with your payment.</p>

    <h3>Next step</h3>

    <p><% h.contact_email('Contact the committee') %></p>

    <p>Your details are:
    person <% c.signed_in_person.id %>,
    registration <% c.signed_in_person.registration.id %>,
    invoice <% c.signed_in_person.invoices[0].id %>.</p>

    <h3>Other option</h3>
    <% h.link_to('View registration details', url=h.url(action='view', id=c.signed_in_person.registration.id)) %><br>

% else:
    <p>Interesting!</p>
% #endif

    <h3>Summary of steps</h3>
% if c.signed_in_person:
    <p><% h.yesno(c.signed_in_person.registration != None) %> Fill in registration form
    <br><% h.yesno(c.signed_in_person.valid_invoice()) %> Generate invoice
    <br><% h.yesno(c.signed_in_person.paid()) %> Pay
    <br><% h.yesno(False) %> Attend conference</p>
% else:
    <p><% h.yesno(False) %> Fill in registration form
    <br><% h.yesno(False) %> Generate invoice
    <br><% h.yesno(False) %> Pay
    <br><% h.yesno(False) %> Attend conference</p>
% #endif
% #endif
