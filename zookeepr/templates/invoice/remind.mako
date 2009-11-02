<%inherit file="/base.mako" />

Send emails as follows.<br>

<h2>NOT_PAID:</h2>

<blockquote>
<p>You have not yet paid invoice $invoice_id</p>
<p>Please go to ${ h.lca_info['event_url'] }/profile/$profile_id to edit your registration and complete your payment.</p>
</blockquote>

<h2>NO_INVOICE:</h2>

<blockquote>
<p>You have not yet paid invoice $invoice_id</p>
<p>Please go to ${ h.lca_info['event_url'] }/profile/$profile_id to edit your registration and complete your payment.</p>
</blockquote>

<h2>INVALID:</h2>

<blockquote>
<p>Ignore these. We need to check them out and fix them up. It means something dodgey has been going on.</p>
</blockquote>

<h2>BAD_PAYMENT:</h2>
<blockquote>
<p>Your attempt to pay invoice $invoice_id, failed. Most likely a problem with your card.</p>
<p>Please go to ${ h.lca_info['event_url'] }/profile/$profile_id to edit your registration and complete your payment.</p>
</blockquote>

<p>
You will need to go to ${ h.link_to('this page', h.url_for(controller='registration', action='remind')) } as well to get those people that havn't generated an invoice yet.
<p>

<strong>firstname,lastname,email_address,profile_id,invoice_id,status</strong><br>
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
%     elif i.bad_payments().count() > 0:
<%         status = "INVALID" %>
%     elif not i.good_payments().count() > 0:
<%         status = "BAD_PAYMENT" %>
%     elif i.good_payments().count() > 0:
<%         continue %>
%     else:
<%         status = "UNKNOWN" %>
%     endif

%     if status == "INVALID":
<strong>
%     endif
"${ i.person.firstname }","${ i.person.lastname }","${ i.person.email_address }",${ i.person.id },${ i.id },${ status }<br/>
%     if status == "INVALID":
</strong>
%     endif
<%     count += 1 %>
% endfor

<p>${ count } invoices not paid</p>

