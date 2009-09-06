<%inherit file="/base.mako" />

    <h2>View special offer</h2>

    <table>
      <tr class="even">
        <td><b>Enabled:</b></td><td>${ h.yesno(c.special_offer.enabled) |n }</td>
      </tr>
      <tr class="odd">
        <td><b>Name:</b></td><td>${ c.special_offer.name  }</td>
      </tr>
      <tr class="even">
        <td valign="top"><b>Description:</b></td><td>${ c.special_offer.description | n}</td>
      </tr>
      <tr class="odd">
        <td valign="top"><b>ID Name:</b></td><td>${ c.special_offer.id_name }</td>
      </tr>
   </table>

    <p>
    ${ h.link_to('Edit', url=h.url_for(action='edit',id=c.special_offer.id)) } |
    ${ h.link_to('Delete', url=h.url_for(action='delete',id=c.special_offer.id)) } |
    ${ h.link_to('Back', url=h.url_for(action='index', id=None)) }</p>
