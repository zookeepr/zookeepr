From: ${ h.lca_info['event_name'] } <${ h.lca_info['contact_email'] }>
To: ${ c.person.firstname } ${ c.person.lastname } <${ c.person.email_address }>
Subject: Confirmation of your miniconf proposal for ${ h.lca_info['event_name'] }

Dear ${ c.person.firstname },

Thankyou for proposing a ${ c.proposal.type.name.lower() } for ${ h.lca_info['event_name'] }

If you have any queries about your proposed ${ c.proposal.type.name.lower() }, please email
${ h.lca_info['speaker_email'] }

title: ${ c.proposal.title }
target audience: ${ c.proposal.audience.name }
url: ${ c.proposal.url }
attachments: ${ len(c.proposal.attachments) }
summary: ${ c.proposal.abstract }

travel assistance: ${ c.travel_assistance }
accom assistance: ${ c.travel_assistance }

Note: requesting assistance, especially travel assistance, may affect
whether or not your ${ c.proposal.type.name.lower() } is accepted.

Your talk may be recorded by the conference.
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
%   endif
%   if c.proposal.slides_release:
You consent to linux.conf.au releasing your slides, if you supply them to
us, under the Creative Commons ShareAlike License.
%   else:
You DO NOT consent to linux.conf.au releasing your slides.
%   endif
% endif
% if c.proposal.video_release or c.proposal.slides_release:

Please make sure that you are allowed to do this, if there is any doubt
(for instance, consider whether you're revealing your employer's
information or using other people's copyrighted materials.)
% endif
% if not c.proposal.video_release or not c.proposal.slides_release:

Please consider allowing us to share both the video of your talk and your
slides, so that the community can gain the maximum benefit from your talk!
% endif

<%doc>
This template is used to generate the email that is sent to people
submitting talks and tutorials for the conference.
</%doc>
