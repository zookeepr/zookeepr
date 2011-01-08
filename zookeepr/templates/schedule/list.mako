<%inherit file="/base.mako" />

<p class="note"><i>Schedule is subject to change without notice.</i></p>

<table id="programme" style="" summary="Programme" cellpadding="" cellspacing="">
  <thead>
    <tr>
      <th>&nbsp;</th>
%for location in c.locations:
      <th class="programme_room">${ location.display_name }</th>
%endfor
    </tr>
  </thead>
  <tbody>
% for time, schedules in c.programme.items():
    <tr>
%   if time in c.primary_times:
<%
      time_slot = c.primary_times[time]
%>
      <th class="programme_slot" rowspan="${ (time_slot.end_time - time_slot.start_time).seconds/60/5 }">
        ${ time_slot.start_time.time().strftime('%H:%M') }<br />
        -<br />
        ${ time_slot.end_time.time().strftime('%H:%M') }
%     if c.can_edit:
        <br />${ h.link_to('Edit', url=h.url_for(controller='time_slot', action='edit', id=time_slot.id)) }
%     endif
      </th>
%   endif
%   if schedules is not None:
%     if 'exclusive' in schedules:
<%
        event = schedules['exclusive'][0].event
        time_slot = schedules['exclusive'][0].time_slot
%>
      <td class="programme_${ event.type.name }" colspan="${ len(c.locations) }" rowspan="${ (time_slot.end_time - time_slot.start_time).seconds/60/5 }">
%       if event.url:
        ${ h.link_to(event.title, url=event.url)}
%       else:
        ${ event.title }
%       endif
        <br />
<%
        locations = event.location_by_time_slot(time_slot)
%>
%       if len(locations) == 1:
        <i>${ locations[0].display_name }</i>
%       else:
        ${ '%s and %s' % (', '.join(location.display_name for location in locations[: -1] ), locations[-1].display_name) }</i>
%       endif
%       if c.can_edit:
        <br />${ h.link_to('Edit', url=h.url_for(controller='event', action='edit', id=event.id)) }
%       endif
      </td>
%     elif 'location' in schedules:
%       for schedule in schedules['location']:
%         if schedule is not None:
<%
            event = schedule.event
            time_slot = schedule.time_slot
%>
      <td class="programme_${event.type.name}" rowspan="${ (time_slot.end_time - time_slot.start_time).seconds/60/5 }">
%           if not time_slot.primary:
        <b>${ time_slot.start_time.time().strftime('%H:%M') }</b>:
%           endif

%           if event.proposal is not None:
        <%include file="talk_link.mako" args="talk_id=event.proposal_id" />
%           elif '::' in event.title:
<%
              miniconf_talk = event.title.split('::')
              miniconf = miniconf_talk[0]
              title = miniconf_talk[1]
              speaker = miniconf_talk[2]
%>
        <%include file="miniconf_talk_link.mako" args="miniconf=miniconf, title=title, speaker=speaker" />
%           else:
%             if event.url:
        ${ h.link_to(event.title, url=event.url) }
%             else:
        ${ event.title }
%             endif
%           endif
%       if c.can_edit:
        <br />${ h.link_to('Edit', url=h.url_for(controller='schedule', action='edit', id=schedule.id)) }
%       endif
      </td>
%         endif
%       endfor
%     endif
%   endif
    </tr>
% endfor
% if c.can_edit:
  <tr>
    <td>${ h.link_to('New TimeSlot', url=h.url_for(controller='time_slot', action='new', id=None)) }</td>
    <td colspan="${ len(c.locations) }">${ h.link_to('Add Event to Schedule', url=h.url_for(controller='schedule', action='new', id=None)) }</td>
  </tr>
% endif
</table>

<p class="note"><i>Schedule is subject to change without notice.</i></p>

<%def name="title()">
Schedule - ${ parent.title() }
</%def>

