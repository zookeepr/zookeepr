      <p>
        <label for="schedule.time_slot">Time Slot:</label>
        ${ h.select('schedule.time_slot', None, [(time_slot.id, time_slot.description) for time_slot in c.time_slots], prompt='None') }
      </p>
      <p>
        <label for="schedule.location">Location:</label>
        ${ h.select('schedule.location', None, [(location.id, location.display_name) for location in c.locations], prompt='None') }
      </p>
      <p>
        <label for="schedule.event">Event:</label>
        ${ h.select('schedule.event', None, [(event.id, event.title) for event in c.events], prompt='None') }
      </p>
