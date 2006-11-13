<h1>Profile</h1>

<div>
<% c.profile.fullname %>
</div>

<%method title>
<% c.profile.handle |h %> profile - <& PARENT:title &>
</%method>
