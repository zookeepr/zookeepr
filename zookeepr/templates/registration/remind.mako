<%inherit file="/base.mako" />

<p>Send emails as follows.</p>

<blockquote>
<p>You have not yet paid your registration</p>
<p>Please go to ${ h.url_for(qualified=True, controller='registration', action='status', id=None)} to edit your registration and complete your payment.</p>
</blockquote>

<p>
You will need to go to ${ h.link_to('this page', h.url_for(controller='invoice', action='remind')) } as well to get those people that have generated an invoice.</p>

<p>
<strong>firstname,lastname,email_address,profile_id,status</strong><br>
<% count = 0 %>
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

"${ r.person.firstname }","${ r.person.lastname }","${ r.person.email_address }",${ r.person.id },NO_INVOICE<br>
<%     count += 1 %>

% endfor
</p>

<p>
${ count } registrations have no invoices
</p>
