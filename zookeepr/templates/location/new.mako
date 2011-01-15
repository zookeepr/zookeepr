<%inherit file="/base.mako" />

    <h2>New Location</h2>

    ${ h.form(h.url_for(action='new')) }
<%include file="form.mako" />
      <p>${ h.submit('button', "New") }
      ${ h.link_to('Back', url=h.url_for(action='index')) }</p>
    ${ h.end_form() }
