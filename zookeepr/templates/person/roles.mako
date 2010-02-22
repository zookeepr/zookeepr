<%inherit file="/base.mako" />
<%def name="toolbox_extra_admin()">
  <li>${ h.link_to('Roles', url=h.url_for(controller='role')) }</li>
  <li>${ h.link_to('Edit Person', url=h.url_for(controller='person', action='edit',id=c.person.id)) }</li>
</%def>

<h2>Modify Roles</h2>

<p><b> ${ c.person.firstname } ${ c.person.lastname } </b></p>
<br>
<table>
% for role in c.roles:
    <tr class="${ h.cycle('even', 'odd') }">
        <td valign="middle">
            <% has = role in c.person.roles %>
            ${ ('is not', 'is')[has] }
        </td>
        <td>
            ${ role.name }
        </td>
        <td>
            ${ h.form(h.url_for()) }
            ${ h.hidden('role', role.name) }
            ${ h.hidden('action', ('Grant', 'Revoke')[has]) }
            ${ h.submit('submit', ('Grant', 'Revoke')[has]) }
            ${ h.end_form() }
        </td>
    </tr>
% endfor
</table>



<%def name="title()">
Roles -
${ c.person.firstname |h } ${ c.person.lastname |h } - 
Roles
${ parent.title() }
</%def>

