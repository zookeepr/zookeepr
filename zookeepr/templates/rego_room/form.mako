<p>
<label for="rego_room.rego">Registration ID:</label>
${ h.text('rego_room.rego', size=10) }
</p>
<p class="room">Enter the registration ID you wish to append this room to. (${ h.link_to('See registration list', h.url_for(controller='registration', action='index')) })</p>

<p>
<label for="rego_room.room">Room number:</label><br />
${ h.textarea('rego_room.room', cols="70", rows="6") }
</p>

<p>
<label for="rego_room.by">By ID:</label>
${ h.text('rego_room.by', size=10) }
</p>

<p class="room">Who is this room posted by (defaults to your ID)? (${ h.link_to('See person list', h.url_for(controller='person', action='index')) })</p>

