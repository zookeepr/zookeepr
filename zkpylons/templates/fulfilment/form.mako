      <p>
        <label for="fulfilment.person">Person:</label>
        ${ h.text('fulfilment.person') }
      </p>
      <p>
        <label for="fulfilment.type">Type:</label>
        ${ h.select('fulfilment.type', '', [(t.id, t.name) for t in c.fulfilment_type], prompt='Please select a type') }
      </p>
      <p>
        <label for="fulfilment.status">Status:</label>
        ${ h.select('fulfilment.status', '', [(s.id, s.name) for s in c.fulfilment_status], prompt='Please select a status') }
      </p>
