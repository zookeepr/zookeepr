<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html lang="en-us">
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <link rel="shortcut icon" href="/images/filledfoot-small.png" type="image/png">
        <link rel="stylesheet" media="screen" href="/screen.css" type="text/css">
        <link rel="stylesheet" media="screen" href="/css/lightbox.css" type="text/css">
        <link rel="stylesheet" media="print" href="/print.css" type="text/css">
    </head>

<body>
<style type="text/css">
body { background: white !important; }

.programme_slot { border: 1px solid black; }
.programme_slot:even { background: #000 !important; border: 2px solid black; }
td.programme_Break { border: 1px solid black; background:#CCF; }
td.programme_presentation { border: 1px solid black; }
td.programme_Dinner { border:1px solid black; background: #CEF;}
td {border: 1px solid black; }
 
/*table tr:nth-child(odd) { background:#CCC; }*/ 

.programme_slot:nth-child(2) { background:red; }

</style>
<div class="netv-post">
<h2>${ c.display_date.strftime('%A %d %B %Y') }</h2>
<table id="programme" style="background-color:white;border: 1px solid black !important" summary="Programme" cellpadding="" cellspacing="" width="100%">
  <thead>
    <tr>
      <th>&nbsp;</th>
%for location in c.locations:
      <th class="programme_room">${ location.display_name }</th>
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
%   if event.url:
        ${ h.link_to(title, url=url)}
%   else:
        ${ title }
%   endif
%   if speakers:
        <i>by</i> <span class="by_speaker">${ speakers | n }</span>
%   endif
        <br />
<%
    schedules = event.schedule_by_time_slot(time_slot)
    locations = [schedule.location.display_name for schedule in schedules]
%>
%   if locations:
        <i>${ h.list_to_string(locations) }</i>
%   endif
%   if c.can_edit:
        <br />${ h.link_to('Event Details', url=h.url_for(controller='event', action='view', id=event.id)) }
%     for schedule in schedules:
        <br />${ h.link_to('Edit Schedule for ' + schedule.location.display_name, url=h.url_for(controller='schedule', action='edit', id=schedule.id)) }
%     endfor
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
      <th>
%       if url:
        ${ h.link_to(title, url=url) }
%       else:
        ${ title }
%       endif
%       if c.can_edit:
        <br />${ h.link_to('Event Details', url=h.url_for(controller='event', action='view', id=event.id)) }
        <br />${ h.link_to('Edit Schedule', url=h.url_for(controller='schedule', action='edit', id=schedule.id)) }
%       endif
      </th>
%     else:
      <td class="programme_${event.type.name}" rowspan="${ (time_slot.end_time - time_slot.start_time).seconds/60/5 }">
%       if not time_slot.primary:
        <b>${ time_slot.start_time.time().strftime('%H:%M') }</b>:
%       endif
%       if url:
        ${ h.link_to(title, url=url) }
%       else:
        ${ title }
%       endif
%       if speakers:
        <i>by</i> <span class="by_speaker">${ speakers | n }</span>
%       endif
%       if c.can_edit:
        <br />${ h.link_to('Event Details', url=h.url_for(controller='event', action='view', id=event.id)) }
        <br />${ h.link_to('Edit Schedule', url=h.url_for(controller='schedule', action='edit', id=schedule.id)) }
%       endif
      </td>
%     endif
%   endif
% endfor
    </tr>
%endfor
%if c.can_edit:
  <tr>
    <td>${ h.link_to('New TimeSlot', url=h.url_for(controller='time_slot', action='new', id=None)) }</td>
    <td colspan="${ len(c.locations) }">${ h.link_to('Add Event to Schedule', url=h.url_for(controller='schedule', action='new', id=None)) }</td>
  </tr>
%endif
</table>
</div>
</body>
</html>
