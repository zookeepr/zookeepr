<%inherit file="/base.mako" />

    <h2>View Product Category</h2>

    <table>
      <tr class="${h.cycle('odd','even')}">
        <td><b>Name:</b></td><td>${ c.product_category.name  }</td>
      </tr>
      <tr class="${h.cycle('odd','even')}">
        <td valign="top"><b>Description:</b></td><td>${ c.product_category.description |n}</td>
      </tr>
      <tr class="${h.cycle('odd','even')}">
        <td valign="top"><b>Note:</b></td><td>${ c.product_category.note }</td>
      </tr>
      <tr class="${h.cycle('odd','even')}">
        <td><b>Display:</b></td><td>${ c.product_category.display }</td>
      </tr>
      <tr class="${h.cycle('odd','even')}">
        <td><b>Display Mode:</b></td><td>${ c.product_category.display_mode }</td>
      </tr>
      <tr class="${h.cycle('odd','even')}">
        <td><b>Display Order:</b></td><td>${ c.product_category.display_order }</td>
      </tr>
      <tr class="${h.cycle('odd','even')}">
        <td><b>Invoice Free Products:</b></td><td>${ h.yesno(c.product_category.invoice_free_products) | n}</td>
      </tr>
      <tr class="${h.cycle('odd','even')}">
        <td><b>Min. Quantity:</b></td><td>${ c.product_category.min_qty }</td>
      </tr>
      <tr class="${h.cycle('odd','even')}">
        <td><b>Max. Quantity:</b></td><td>${ c.product_category.max_qty }</td>
      </tr>
   </table>

    <p>
    ${ h.link_to('Edit', url=h.url_for(action='edit',id=c.product_category.id)) } |
    ${ h.link_to('Back', url=h.url_for(action='index', id=None)) }</p>
