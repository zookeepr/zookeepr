<%page args="fulfilment" />
    <h3>${ fulfilment.type.name } - ${ fulfilment.id }</h3>

    <p><b>Status:</b> ${ fulfilment.status.name }<br></p>
    <p><b>Void:</b> ${ h.yesno(fulfilment.is_void) |n }<br></p>
    <p><b>Completed:</b> ${ h.yesno(fulfilment.is_completed) |n }<br></p>
    <p><b>Locked:</b> ${ h.yesno(fulfilment.is_locked) |n }<br></p>
    <p><b>Can Edit:</b> ${ h.yesno(fulfilment.can_edit) |n }<br></p>
    <table>
      <tr>
        <th>Product</th>
        <th>Product Text</th>
        <th>Qty</th>
      </tr>
% for item in fulfilment.items:
      <tr>
        <td>${ item.product.category.name } - ${ item.product.description }</td>
        <td>${ item.product_text }</td>
        <td>${ item.qty }</td>
      </tr>
% endfor
    </table>
    <p>
% if c.can_edit:
      ${ h.link_to('Edit', url=h.url_for(action='edit')) } |
% endif
      ${ h.link_to('Back', url=h.url_for(action='index', id=None)) }
    </p>
