<%inherit file="/base.mako" />
<%
    c.form = 'new'
%>
<h1>New user account creation</h1>

<p class="lead">Enter your name, and email address, and password, and we'll email you with a confirmation to create your account.</p>

<p class="lead">
If you've already got an account but can't log in, you can
${ h.link_to('recover your password', url=h.url_for(action='forgotten_password')) }.
</p>

<form action="/person/new" method="post" data-toggle="validator">
<%include file="form.mako" />

  <div class="form-group">
    <button type="submit" class="btn btn-primary">Create a new account</button>
  </div>


${ h.end_form() }

