      <p>
        <label for="fulfilment_type.name">Name:</label>
        ${ h.text('fulfilment_type.name') }
      </p>
      <p>
        <label for="fulfilment_type.initial_status">Initial Status:</label>
        ${ h.select('fulfilment_type.initial_status', None, [(s.id, s.name) for s in c.fulfilment_status], prompt='Please select an initial status') }
      </p>
      <p>
        <label for="fulfilment_type.status">Status available for this type:</label>
        ${ h.select('fulfilment_type.status', None, [(s.id, s.name) for s in c.fulfilment_status], multiple=True) }
      </p>
