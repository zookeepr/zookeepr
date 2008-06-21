<h2><% c.person.firstname |h %>'s profile</h2>

<div class="boxed">

<p>
   <b>Email:</b>
    <% c.person.email_address | h %><br>
</p>

<p>
   <b>First name:</b>
    <% c.person.firstname | h %><br>
</p>

<p>
   <b>Last name:</b>
    <% c.person.lastname | h %><br>
</p>
</div>

<p>
   <b>Phone:</b>
<% c.person.phone %><br>
</p>

<p>
<b>Mobile:</b>
<% c.person.mobile %>
</p>

<hr />

#% if c.can_edit:
#<% h.link_to('Edit', url=h.url(action='edit',id=c.person.get_unique())) %> |
#% #end if
#<% h.link_to('Back', url=h.url(action='index')) %>

<%method title>
Profile -
<% c.person.firstname |h %> <% c.person.lastname |h %> -
<& PARENT:title &>
</%method>
