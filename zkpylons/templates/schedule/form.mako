      <p>
        <label for="schedule.time_slot">Time Slot:</label>
        ${ h.select('schedule.time_slot', None, [(time_slot.id, time_slot.description) for time_slot in c.time_slots], prompt='None') }
        <br />-- OR --<br />
        ${ h.link_to('Add Time Slot', h.url_for(controller='time_slot', action='new', id=None)) }
      </p>
      <p>
        <label for="schedule.location">Location:</label>
        ${ h.select('schedule.location', None, [(location.id, location.display_name) for location in c.locations], prompt='None') }
        <br />-- OR --<br />
        ${ h.link_to('Add Location', h.url_for(controller='location', action='new', id=None)) }
      <p>
        <label for="schedule.event">Event:</label>
        ${ h.select('schedule.event', None, [(event.id, str(event.proposal_id or event.computed_miniconf()) + ' - ' + event.computed_title()) for event in c.events], prompt='None') }
        <br />-- OR --<br />
        ${ h.link_to('Add Event', h.url_for(controller='event', action='new', id=None)) }
      </p>
      <p>
        <label for="schedule.video_url">Video URL:</label>
        ${ h.text('schedule.video_url') }
      </p>
      <p>
        <label for="schedule.audio_url">Audio URL:</label>
        ${ h.text('schedule.audio_url') }
      </p>
      <p>
        <label for="schedule.slides_url">Slides URL:</label>
        ${ h.text('schedule.slide_url') }
      </p>
      <p>
        ${ h.checkbox('schedule.overflow', label='Is overflow event (Should not be ticked in most cases)') }
      </p>

