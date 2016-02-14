      <p>
        <label for="time_slot.start_date">Start Date (dd/mm/yyyy):</label>
        ${ h.text('time_slot.start_date') }
      </p>

      <p>
        <label for="time_slot.start_time">Start Time (hh:mm):</label>
        ${ h.text('time_slot.start_time') }
      </p>

      <p>
        <label for="time_slot.end_date">End Date (dd/mm/yyyy):</label>
        ${ h.text('time_slot.end_date') }
      </p>

      <p>
        <label for="time_slot.end_time">End Time (hh:mm):</label>
        ${ h.text('time_slot.end_time') }
      </p>
      <p>
        ${ h.checkbox('time_slot.primary', label='Primary Timeslot') }
        <sub>Should this TimeSlot be used to generate the time scale on the side of the schedule</sub>
      </p>
      <p>
        ${ h.checkbox('time_slot.heading', label='Heading') }
        <sub>Should this TimeSlot be used to display a heading instead of a normal event</sub>
      </p>
