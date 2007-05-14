<pre>
Subject: Confirmation of your miniconf proposal for linux.conf.au 2008
To: <% c.person.firstname %> <% c.person.lastname %> <<% c.person.email_address %>>

Dear <% c.person.firstname %>,

Thankyou for proposing a miniconf for linux.conf.au 2008

title: <% c.proposal.title %>
url: <% c.proposal.url %>
attachments: <% len(c.proposal.attachments) %>
summary: <% c.proposal.abstract %>

<%doc>
This template is used to generate the email that is sent to people
submitting miniconfs and/or papers for the conference.
</%doc>
