From: ${ h.lca_info['event_name'] } <${ h.lca_info['contact_email'] }>
To: ${ c.person.firstname } ${ c.person.lastname } <${ c.person.email_address }>
Subject: Confirmation of your ${ c.proposal.type.name.lower() } proposal for ${ h.lca_info['event_name'] }

Dear ${ c.person.firstname },

Thank you for proposing a ${ c.proposal.type.name.lower() } for ${ h.lca_info['event_name'] }.

If you have any queries about your proposed ${ c.proposal.type.name.lower()},
please email ${ c.proposal.type.notify_email.lower() }

Title:             ${ c.proposal.title |n }
Target audience:   ${ c.proposal.audience.name }
URL:               ${ c.proposal.url }
Attachments:       ${ len(c.proposal.attachments) }
Summary:           ${ c.proposal.abstract }

Your ${ c.proposal.type.name.lower() } may be recorded by the conference.
% if c.proposal.video_release and c.proposal.slides_release:
You consent to ${ h.lca_info["event_parent_organisation"] } releasing both the video of your ${ c.proposal.type.name.lower() } and your slides, if you supply them to us, under the ${ h.lca_info["media_license_name"] }.
% else:
%   if c.proposal.video_release:
You consent to ${ h.lca_info["event_parent_organisation"] } releasing the video of your ${ c.proposal.type.name.lower() } under the ${ h.lca_info["media_license_name"] }.
%   else:
You DO NOT consent to ${ h.lca_info["event_parent_organisation"] } releasing the video of your ${ c.proposal.type.name.lower() }.
%   endif
%   if c.proposal.slides_release:
You consent to ${ h.lca_info["event_parent_organisation"] } releasing your slides, if you supply them to us, under the ${ h.lca_info["media_license_name"] }.
%   else:
You DO NOT consent to ${ h.lca_info["event_parent_organisation"] } releasing your slides.
%   endif
% endif
% if c.proposal.video_release or c.proposal.slides_release:

Please make sure that you are allowed to do this, if there is any doubt
(for instance, consider whether you're revealing your employer's
information or using other people's copyrighted materials.)
% endif
% if not c.proposal.video_release or not c.proposal.slides_release:

Please consider allowing us to share both the video of your
${c.proposal.type.name.lower()} and your slides, so that the community can
gain the maximum benefit from your ${c.proposal.type.name.lower()}!
% endif

Should you need to update the details of this proposal, please use the follow
URL:

  http://${ h.host_name() }/proposal


The ${ h.event_name() } team
http://${ h.host_name() }/contact
