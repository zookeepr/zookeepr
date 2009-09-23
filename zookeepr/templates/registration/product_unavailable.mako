<%inherit file="/base.mako" />

    <h2>Product Unavailable</h2>
    <div>
      <p>Unfortunatly the product ${ c.product.description } is no longer available. To rectify this issue you will need to modify your ${ h.link_to("registration", url=h.url_for(action="edit", id=c.registration.id)) }.</p>
    </div>
