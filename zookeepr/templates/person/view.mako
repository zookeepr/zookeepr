<%inherit file="/base.mako" />
<h2>${ c.person.firstname |h }'s profile</h2>

<table>
    <tr>
        <td><p><b>First name:</b></p></td>
        <td><p>${ c.person.firstname | h }</p></td>
    </tr>
    <tr>
        <td><p><b>Last name:</b></p></td>
        <td><p>${ c.person.lastname | h }</p></td>
    </tr>
    <tr>
        <td><p><b>Email:</b></p></td>
        <td><p>${ c.person.email_address | h }</p></td>
    </tr>
% if c.person.phone:
    <tr>
        <td><p><b>Phone:</b></p></td>
        <td><p>${ c.person.phone | h }</p></td>
    </tr>
% endif
% if c.person.mobile:
    <tr>
        <td><p><b>Mobile:</b></p></td>
        <td><p>${ c.person.mobile | h }</p></td>
    </tr>
% endif
% if c.person.company:
    <tr>
        <td><p><b>Company:</b></p></td>
        <td><p>${ c.person.company | h }</p></td>
    </tr>
% endif
    <tr>
        <td valign="top"><p><b>Address:</b></p></td>
        <td><p>${ c.person.address1 |h }<br>
% if c.person.address2:
                ${ c.person.address2 |h }<br>
% endif
                ${ c.person.city |h }<br>
                ${ c.person.state |h } ${ c.person.postcode |h }<br>
                ${ c.person.country |h }</p></td>
    </tr>
</table>

<hr>

% if h.auth.authorized(h.auth.Or(h.auth.is_same_zookeepr_user(c.person.id), h.auth.has_organiser_role)):
<ul><li>${ h.link_to('Edit', url=h.url_for(action='edit',id=c.person.id)) }</li></ul>
% endif

<%def name="title()">
Profile -
${ c.person.firstname |h } ${ c.person.lastname |h } -
 ${ parent.title() }
</%def>
