<%inherit file="/base.mako" />

<h2>Accept Volunteer</h2>

${ h.form(h.url_for()) }
      <p>Please choose the ticket type that the volunteer will be eligible for:</p>
      ${ h.select('ticket_type', '', c.products_select) }

<p>${ h.submit("submit", "Accept") }

${ h.end_form() }
