      <p>
        <label for="fulfilment_status.name">Name:</label>
        ${ h.text('fulfilment_status.name') }
      </p>
      <p>
        <label for="fulfilment_status.void">Void:</label>
        ${ h.checkbox('fulfilment_status.void') }<br />
        <sub>Does this status mark the Fulfilment void</sub>
      </p>
      <p>
        <label for="fulfilment_status.completed">Completed:</label>
        ${ h.checkbox('fulfilment_status.completed') }<br />
        <sub>Does this status mark the Fulfilment completed</sub>
      </p>
      <p>
        <label for="fulfilment_status.locked">Locked:</label>
        ${ h.checkbox('fulfilment_status.locked') }<br />
        <sub>Does this status mark the Fulfilment locked</sub>
      </p>
      <p>
        <label for"fulfilment_status.types">Types:</label>
        ${ h.select('fulfilment_status.types', None, [(ft.id, ft.name) for ft in c.fulfilment_types], multiple=True) }<br />
        <sub>What types can use this status</sub>
      </p>
