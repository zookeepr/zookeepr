<%inherit file="/base.mako" />

Send emails as follows.<br>

<h2>NOT_PAID:</h2>
You have not yet paid invoice $invoice_id<br>
Please go to http://${ h.host_name() }/profile/$profile_id to edit your registration and complete your payment.

<h2>NO_INVOICE:</h2>
You have not yet paid invoice $invoice_id<br>
Please go to http://${ h.host_name() }/profile/$profile_id to edit your registration and complete your payment.

<h2>INVALID:</h2>
Ignore these. JF needs to check them out and fix them up. It means something dodgey has been going on

<h2>BAD_PAYMENT:</h2>
Your attempt to pay invoice $invoice_id, failed. Most likely a problem with your card.<br>
Please go to http://${ h.host_name() }/profile/$profile_id to edit your registration and complete your payment.<br>

<p>

You will need to go to http://${ h.host_name() }/registration/remind as well to get those people that havn't generated an invoice yet.
<p>

<strong>firstname,lastname,email_address,profile_id,status,earlybird</strong><br>
<% count = 0 %>
% for i in c.invoice_collection:
<%     speaker = False %>
%     if i.person.proposals:
%         for proposal in i.person.proposals:
%             if proposal.accepted:
<%                 speaker = True %>
%             endif
%         endfor
%         if speaker:
<%             continue %>
%         endif
%     endif
<%     status = "" %>
%     if i.total() == 0:
<%         continue %>
%     elif not i.payments:
<%         status = "NOT_PAID" %>
%     elif i.bad_payments:
<%         status = "INVALID" %>
%     elif not i.good_payments:
<%         status = "BAD_PAYMENT" %>
%     elif i.good_payments:
<%         continue %>
%     else:
<%         status = "UNKNOWN" %>
%     endif

%     if status == "INVALID":
<strong>
%     endif
"${ i.person.firstname }","${ i.person.lastname }","${ i.person.email_address }",${ i.person.id },${ status },${ c.payment_options.is_earlybird(i.person.registration.creation_timestamp) }<br/>
%     if status == "INVALID":
</strong>
%     endif
<%     count += 1 %>
% endfor

<p>${ count } invoices not paid</p>

