
Send emails as follows.<br>

You have not yet paid your rego<br>
Please go to http://lca2007.linux.org.au/profile/$profile_id to edit your registration and complete your payment.
<p>

You will need to go to http://lca2007.linux.org.au/invoice/remind as well to get those people that have generated an invoice.
<p>

<strong>firstname,lastname,email_address,profile_id</strong><br>
% count = 0
% for r in registrations:
%     speaker = False
%     if r.person.proposals:
%         for proposal in r.person.proposals:
%             if proposal.accepted:
%                 speaker = True
%             # endif
%         # endfor
%         if speaker:
%             continue
%         # endif
%     # endif
%     if r.person.invoices:
%         continue
%     # endif

"<% r.person.firstname %>","<% r.person.lastname %>","<% r.person.email_address %>",<% r.person.id %><br>
%     count += 1

% # endfor

<p>
<% count %> registrations have no invoices

<%init>

registrations = c.registration_collection

</%init>
