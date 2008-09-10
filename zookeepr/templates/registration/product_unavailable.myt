    <h2>Product Unavailable</h2>
    <div>
      <p>Unfortunatly the product <% product.description %> is no longer available. To rectify this issue you will need to modify your <% h.link_to("registration", url=h.url(action="edit", id=c.registration.id)) %>.</p>
    </div>

<%args>
product
</%args>
