<h2>Modify Roles</h2>

<% c.res %>

<%method title>
Profile -
<% c.person.firstname |h %> <% c.person.lastname |h %> -
Roles
<& PARENT:title &>
</%method>
