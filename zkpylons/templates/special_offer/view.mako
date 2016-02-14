<%inherit file="/base.mako" />

    <h2>View Special Offer</h2>

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

%if c.registrations.count() > 0:
    <p>People who took advantage of this offer:
    <ul>
%  for rego in c.registrations:
        <li>${ h.link_to(rego.person.firstname + ' ' + rego.person.lastname, url=h.url_for(controller='person', action='view', id=rego.person.id)) }: '${rego.member_number }' --
%    if rego.person.registration:
${ h.link_to('registered', url=h.url_for(controller='registration', action='view', id=rego.person.registration.id)) }
%      if rego.person.paid():
and paid
%      else:
but not paid
%      endif
%    else:
not registered
%    endif
</li>
%  endfor
    </ul>
%endif
    </p>
    <p>
    ${ h.link_to('Edit', url=h.url_for(action='edit',id=c.special_offer.id)) } |
    ${ h.link_to('Delete', url=h.url_for(action='delete',id=c.special_offer.id)) } |
    ${ h.link_to('Back', url=h.url_for(action='index', id=None)) }</p>
