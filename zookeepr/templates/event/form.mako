      <p>
        <label for="event.type">Event Type:</label>
        ${ h.select('event.type', None, [(event_type.id, event_type.name) for event_type in c.event_types], prompt='None') }
      </p>
      <p>
        <label for="event.proposal">Proposal:</label>
        ${ h.select('event.proposal', None, [(proposal.id, proposal.title) for proposal in c.proposals], prompt='None') }
      </p>
      <p>
        <label for="event.title">Title:</label>
        ${ h.text('event.title') }
      </p>
      <p>
        <label for="event.url">URL:</label>
        ${ h.text('event.url') }
      </p>
      <p>
        ${ h.checkbox('event.publish', label='Publish Event') }
        <sub>Publish this event in the public schedule</sub>
      </p>
      <p>
        ${ h.checkbox('event.exclusive', label='Exclusive') }
        <sub>Is this event the only one in all of it's scheduled timeslots</sub>
      </p>
