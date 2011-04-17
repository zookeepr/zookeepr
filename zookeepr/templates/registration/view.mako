<%inherit file="/base.mako" />

        <h2>Your registration details</h2>
        <p>Here are the registration details we have for you.</p>

<%include file="view_body.mako"/>

% if c.registration.person.is_speaker():
          <h2>Speaker recording consent and release</h2>
          <p>As a service to Linux Australia members and to other interested Linux users,
          Linux Australia would like to make your presentation available to the public.
          This involves video­taping your talk, and offering the video/audio and slides
          (for download, or on CD­ROM).</p>

% endif

          <p>${ h.link_to('Edit details', h.url_for(action='edit', id=c.registration.id)) } - ${ h.link_to('back', url=h.url_for(action='status', id=None)) }<br>
