From: <% h.lca_info['event_name'] %> <<% h.lca_info['contact_email'] %>>
To: <% c.person.firstname %> <% c.person.lastname %> <<% c.person.email_address %>>
Subject: Confirmation of your miniconf proposal for <% h.lca_info['event_name'] %>

Dear <% c.person.firstname %>,

Thankyou for proposing a <% c.proposal.type.name.lower() %> for <% h.lca_info['event_name'] %>

If you have any queries about your proposed <% c.proposal.type.name.lower() %>, please email
<% h.lca_info['speaker_email'] %>

title: <% c.proposal.title %>
target audience: <% c.proposal.audience.name %>
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
