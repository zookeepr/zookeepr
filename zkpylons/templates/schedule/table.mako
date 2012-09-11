<%!
def inherit(context):
    c = context.get('c', UNDEFINED)
    if c.raw:
        return '/raw.mako'
    else:
        return '/base.mako'
%>
<%inherit file="${inherit(context)}"/>

<h2>${ c.display_date.strftime('%A %d %B %Y') }</h2>

<p class="note"><i>Schedule is subject to change without notice.</i></p>

<table id="programme" style="" summary="Programme" cellpadding="" cellspacing="">
  <thead>
    <tr>
      <th>&nbsp;</th>
%for location in c.locations:
      <th class="programme_room">
        ${ location.display_name }
%     if c.can_edit:
        <br />${ h.link_to('Edit', url=h.url_for(controller='location', action='edit', id=location.id)) }
%     endif
      </th>
%endfor
    </tr>
  </thead>
  <tbody>
%for time, events in c.programme.items():
    <tr>
% if time in c.primary_times:
<%
    time_slot = c.primary_times[time]
%>
%   if time_slot.heading:
      <th>
        &nbsp;
%     if c.can_edit:
        <br />${ h.link_to('Edit', url=h.url_for(controller='time_slot', action='edit', id=time_slot.id)) }
%     endif
      </th>
%   else:
      <th class="programme_slot" rowspan="${ (time_slot.end_time - time_slot.start_time).seconds/60/5 }">
        ${ time_slot.start_time.time().strftime('%H:%M') }<br />
        -<br />
        ${ time_slot.end_time.time().strftime('%H:%M') }
%     if c.can_edit:
        <br />${ h.link_to('Edit', url=h.url_for(controller='time_slot', action='edit', id=time_slot.id)) }
%     endif
      </th>
%   endif
% endif
% if 'exclusive' in events:
<%
    event = events['exclusive']
    title = event.computed_title()
    speakers = h.list_to_string(event.computed_speakers(), primary_join='%s <i>and</i> %s', html=True)

    if event.proposal:
      url = h.url_for(controller='schedule', action='view_talk', id=event.proposal.id)
    elif event.is_miniconf():
      url = '/wiki/Miniconfs/' + event.computed_miniconf() + 'Miniconf/' + h.wiki_link(event.computed_title())
    else:
      url = event.url
%>
      <td class="programme_${ event.type.name }" colspan="${ len(c.locations) }" rowspan="${ (time_slot.end_time - time_slot.start_time).seconds/60/5 }">
%   if event.publish or c.can_edit:
%     if event.url:
        ${ h.link_to(title, url=url)}
%     else:
        ${ title }
%     endif
%     if speakers:
        <i>by</i> <span class="by_speaker">${ speakers | n }</span>
%     endif
        <br />
%     for schedule in event.schedule_by_time_slot(time_slot):
          <i>${ schedule.location.display_name }</i>
%       if schedule.video_url or schedule.audio_url or schedule.slide_url or c.can_edit:
        <span style="font-size: 8pt;">[
%         if schedule.video_url:
          <a href="${ schedule.video_url }">Video</a> 
%         endif
%         if schedule.audio_url:
          <a href="${ schedule.audio_url }">Audio</a> 
%         endif
%         if schedule.slide_url:
          <a href="${ schedule.slide_url }">Slides</a> 
%         endif
%         if c.can_edit:
          ${ h.link_to('Edit Schedule for ' + schedule.location.display_name, url=h.url_for(controller='schedule', action='edit', id=schedule.id)) }
%         endif
        ]</span>
%       endif
%     endfor
%     if c.can_edit:
        <br />${ h.link_to('Event Details', url=h.url_for(controller='event', action='view', id=event.id)) }
%     endif
%   endif
      </td>
% endif
% for location in c.locations:
%   if location in events:
<%
      schedule = events[location]
      event = schedule.event
      time_slot = schedule.time_slot
      title = event.computed_title()
      speakers = h.list_to_string(event.computed_speakers(), primary_join='%s <i>and</i> %s', html=True)

      if event.proposal:
        url = h.url_for(controller='schedule', action='view_talk', id=event.proposal.id)
      elif event.is_miniconf():
        url = '/wiki/Miniconfs/' + event.computed_miniconf() + 'Miniconf/' + h.wiki_link(event.computed_title())
      else:
        url = event.url
%>
%     if time_slot.heading:
      <th class="programme_${event.type.name}">
%     else:
      <td class="programme_${event.type.name}" rowspan="${ (time_slot.end_time - time_slot.start_time).seconds/60/5 }">
%     endif
%     if event.publish or c.can_edit:
%       if not time_slot.primary:
        <b>${ time_slot.start_time.time().strftime('%H:%M') }</b>:
%       endif
%       if url:
        ${ h.link_to(title, url=url) }
%       else:
        ${ title }
%       endif
%       if speakers and not time_slot.heading:
        <i>by</i> <span class="by_speaker">${ speakers | n }</span>
%       endif
%       if schedule.video_url or schedule.audio_url or schedule.slide_url:
        <span style="font-size: 8pt;">[
%         if schedule.video_url:
          <a href="${ schedule.video_url }">Video</a> 
%         endif
%         if schedule.audio_url:
          <a href="${ schedule.audio_url }">Audio</a> 
%         endif
%         if schedule.slide_url:
          <a href="${ schedule.slide_url }">Slides</a> 
%         endif
        ]</span>
%       endif
%     endif
%     if c.can_edit:
        <br />${ h.link_to('Event Details', url=h.url_for(controller='event', action='view', id=event.id)) }
        <br />${ h.link_to('Edit Schedule', url=h.url_for(controller='schedule', action='edit', id=schedule.id)) }
%     endif
%     if time_slot.heading:
      </th>
%     else:
      </td>
%     endif
%   endif
% endfor
    </tr>
%endfor
%if c.can_edit:
  <tr>
    <td>${ h.link_to('New TimeSlot', url=h.url_for(controller='time_slot', action='new', id=None)) } ${ h.link_to('New Location', url=h.url_for(controller='location', action='new', id=None)) }</td>
    <td colspan="${ len(c.locations) }">${ h.link_to('Add Event to Schedule', url=h.url_for(controller='schedule', action='new', id=None)) }</td>
  </tr>
%endif
</table>

<p class="note"><i>Schedule is subject to change without notice.</i></p>

<%def name="title()">
Schedule - ${ parent.title() }
</%def>
