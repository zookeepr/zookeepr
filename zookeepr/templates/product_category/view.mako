<%inherit file="/base.mako" />

    <h2>View product category</h2>

    <table>
      <tr class="odd">
        <td><b>Name:</b></td><td>${ c.product_category.name  }</td>
      </tr>
      <tr class="even">
        <td valign="top"><b>Description:</b></td><td>${ c.product_category.description }</td>
      </tr>
      <tr class="odd">
        <td valign="top"><b>Note:</b></td><td>${ c.product_category.note }</td>
      </tr>
      <tr class="even">
        <td><b>Display:</b></td><td>${ c.product_category.display }</td>
      </tr>
      <tr class="odd">
        <td><b>Display in a Grid:</b></td><td>${ c.product_category.display_grid }</td>
      </tr>
      <tr class="even">
        <td><b>Display Order:</b></td><td>${ c.product_category.display_order }</td>
      </tr>
      <tr class="odd">
        <td><b>Min. Quantity:</b></td><td>${ c.product_category.min_qty }</td>
      </tr>
      <tr class="even">
        <td><b>Max. Quantity:</b></td><td>${ c.product_category.max_qty }</td>
      </tr>
   </table>

    <p>
    ${ h.link_to('Edit', url=h.url_for(action='edit',id=c.product_category.id)) } |
    ${ h.link_to('Back', url=h.url_for(action='index', id=None)) }</p>
