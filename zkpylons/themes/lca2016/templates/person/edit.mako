<%inherit file="/base.mako" />
<h2>Edit profile</h2>

<div class="alert alert-info" role="alert">If you need to change your password you may use the ${ h.link_to("Forgotten Password Service", url=h.url_for(controller='person', action='forgotten_password')) }.</div>

${ h.form(h.url_for(id=c.person.id)) }

<%include file="form.mako" />

  <div class="form-group">
    <input id="update" type="submit" name="update" value="Update" class="btn btn-primary">
  </div>


${ h.end_form() }

