From: <% h.lca_info['event_name'] %> <<% h.lca_info['contact_email'] %>>
To: <% c.person.firstname %> <% c.person.lastname %> <<% c.person.email_address %>>
Subject: Confirmation of your <% c.proposal.type.name.lower() %> proposal for <% h.lca_info['event_name'] %>

Dear <% c.person.firstname %>,

Thank you for proposing a <% c.proposal.type.name.lower() %> for <% h.lca_info['event_name'] %>

Please make sure that these details are correct. If you need to change
anything, log into your account at:

  <% h.lca_info['event_url'] %>

  Title:           <% c.proposal.title %>
  Target Audience: <% c.proposal.audience.name %>
  URL:             <% c.proposal.url %>
  Attachments:     <% len(c.proposal.attachments) %>
  Summary:         <% c.proposal.abstract %>

  Travel Assistance:        <% c.travel_assistance %>
  Accommodation Assistance: <% c.travel_assistance %>

Note that requesting assistance, especially travel assistance, may
affect whether or not your <% c.proposal.type.name.lower() %> is
accepted.

Your presentation may be recorded by the conference.
% if c.proposal.video_release and c.proposal.slides_release:
You consent to linux.conf.au releasing both the video of your talk and your
slides, if you supply them to us, under the Creative Commons ShareAlike
License.
% else:
%   if c.proposal.video_release:
You consent to linux.conf.au releasing the video of your talk under the
Creative Commons ShareAlike License.
%   else:
You DO NOT consent to linux.conf.au releasing the video of your talk.
%   #endif
%   if c.proposal.slides_release:
You consent to linux.conf.au releasing your slides, if you supply them to
us, under the Creative Commons ShareAlike License.
%   else:
You DO NOT consent to linux.conf.au releasing your slides.
%   #endif
% #endif
% if c.proposal.video_release or c.proposal.slides_release:

Please make sure that you are allowed to do this and have your
employer's permission if necessary.

% #endif

If you have any problems, feel free to email <% h.lca_info['contact_email'] %>.

Regards,

The <% h.lca_info['event_name'] %> team

<%doc>
This template is used to generate the email that is sent to people
submitting talks and tutorials for the conference.
</%doc>
