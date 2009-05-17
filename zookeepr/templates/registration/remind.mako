<%inherit file="/base.mako" />

Send emails as follows.<br>

You have not yet paid your registration<br>
Please go to http://${ h.host_name() }/profile/$profile_id to edit your registration and complete your payment.
<p>

You will need to go to http://${ h.host_name() }/invoice/remind as well to get those people that have generated an invoice.
<p>

<strong>firstname,lastname,email_address,profile_id,status,earlybird</strong><br>
<% count = 0 %>
<% p = PaymentOptions() %>
% for r in c.registration_collection:
<%     speaker = False %>
%     if r.person.proposals:
%         for proposal in r.person.proposals:
%             if proposal.accepted:
<%                 speaker = True %>
%             endif
%         endfor
%         if speaker:
<%             continue %>
%         endif
%     endif
%     if r.person.invoices:
<%         continue %>
%     endif

"${ r.person.firstname }","${ r.person.lastname }","${ r.person.email_address }",${ r.person.id },NO_INVOICE, ${ p.is_earlybird(r.creation_timestamp) }<br>
%     count += 1

% endfor

<p>
${ count } registrations have no invoices
