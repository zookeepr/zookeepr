<%inherit file="/base.mako" />
<h2>Modify Roles</h2>

<p><b> ${ c.person.firstname } ${ c.person.lastname } </b></p>
<br>
<table>
% for role in c.roles:
    <tr>
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
Profile -
${ c.person.firstname |h } ${ c.person.lastname |h } - 
Roles
${ caller.title() }
</%def>

