From: ${ c.config.get('event_name') } <${ c.config.get('contact_email') }>
To: ${ c.person.firstname } ${ c.person.lastname } <${ c.person.email_address }>
Subject: Confirmation of your ${ c.proposal.type.name.lower() } proposal for ${ c.config.get('event_name') }

Dear ${ c.person.firstname },

Thank you for proposing a ${ c.proposal.type.name.lower() } for ${ c.config.get('event_name') }.

% if c.proposal.type.notify_email:
If you have any queries about your proposed ${ c.proposal.type.name.lower()},
please email ${ c.proposal.type.notify_email.lower() }
% endif

Title:             ${ c.proposal.title |n }
Target audience:   ${ c.proposal.audience.name }
URL:               ${ c.proposal.url }
Attachments:       ${ len(c.proposal.attachments) }
Summary:           ${ c.proposal.abstract }

Travel assistance: ${ c.proposal.travel_assistance.name }
Accom assistance:  ${ c.proposal.accommodation_assistance.name }
%if c.proposal.travel_assistance.id > 1 or c.proposal.accommodation_assistance.id > 1:

Note: requesting assistance, especially travel assistance, may affect
whether or not your ${ c.proposal.type.name.lower() } is accepted.
%endif

Your ${ c.proposal.type.name.lower() } may be recorded by the conference.
% if c.proposal.video_release and c.proposal.slides_release:
You consent to ${ c.config.get("event_parent_organisation") } releasing both the video of your ${ c.proposal.type.name.lower() } and your slides, if you supply them to us, under the ${ c.config.get("media_license_name") }.
% else:
%   if c.proposal.video_release:
You consent to ${ c.config.get("event_parent_organisation") } releasing the video of your ${ c.proposal.type.name.lower() } under the ${ c.config.get("media_license_name") }.
%   else:
You DO NOT consent to ${ c.config.get("event_parent_organisation") } releasing the video of your ${ c.proposal.type.name.lower() }.
%   endif
%   if c.proposal.slides_release:
You consent to ${ c.config.get("event_parent_organisation") } releasing your slides, if you supply them to us, under the ${ c.config.get("media_license_name") }.
%   else:
You DO NOT consent to ${ c.config.get("event_parent_organisation") } releasing your slides.
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

  http://${ c.config.get('event_host') }/proposal


The ${ c.config.get('event_name') } team
http://${ c.config.get('event_host') }/contact
