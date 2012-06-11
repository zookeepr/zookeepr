<%inherit file="/base.mako" />
    <h2>Fingerprint Generation</h2>
    <div id="fingerprint">
      ${ h.form(h.url_for()) }
        <p>
          <label for="keyid">Key ID:</label>
          ${ h.textfield('keyid', size=8) }
        </p>
        <p>${ h.submit('submit', 'Generate') }</p>
      ${ h.end_form() }
    </div>
