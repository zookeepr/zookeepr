Subject: Confirmation of your miniconf proposal for <% h.lca_info['event_name'] %>
To: <% c.person.firstname %> <% c.person.lastname %> <<% c.person.email_address %>>

Dear <% c.person.firstname %>,

Thankyou for proposing a miniconf for <% h.lca_info['event_name'] %>

title: <% c.proposal.title %>
target audience: <% c.proposal.audience %>
url: <% c.proposal.url %>
attachments: <% len(c.proposal.attachments) %>
summary: <% c.proposal.abstract %>

travel assistance: <% c.travel_assistance %>
accom assistance: <% c.travel_assistance %>

Note: requesting assistance, especially travel assistance, may affect
whether or not your <% c.proposal.type.name.lower() %> is accepted.


<%doc>
This template is used to generate the email that is sent to people
submitting talks and tutorials for the conference.
</%doc>
