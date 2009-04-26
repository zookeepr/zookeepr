<%inherit file="/base.mako" />

    <h2>View product category</h2>

    <p><b>Name:</b> ${ c.product_category.name }<br></p>
    <p><b>Description:</b> ${ c.product_category.description }<br></p>
    <p><b>Display:</b> ${ c.product_category.display }<br></p>
    <p><b>Min. Quantity:</b> ${ c.product_category.min_qty }<br></p>
    <p><b>Max. Quantity:</b> ${ c.product_category.max_qty }<br></p>

    <p>
    ${ h.link_to('Edit', url=h.url_for(action='edit',id=c.product_category.id)) } |
    ${ h.link_to('Back', url=h.url_for(action='index', id=None)) }</p>
