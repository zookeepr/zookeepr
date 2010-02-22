<%inherit file="/base.mako" />

    <h2>New Social Network</h2>

    ${ h.form(h.url_for(action='new')) }
<%include file="form.mako" />
      <p>${ h.submit('button', "New") }
      ${ h.link_to('Back', url=h.url_for(action='index')) }</p>
    ${ h.end_form() }

<%def name="title()">
Social Network -
New -
 ${ parent.title() }
</%def>
