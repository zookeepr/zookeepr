<%inherit file="/base.mako" />

    <h2>Edit Social Network</h2>

    ${ h.form(h.url_for(id=c.social_network.id)) }
<%include file="form.mako" />
      <p>${ h.submit('submit', 'Update') } ${ h.link_to('back', url=h.url_for(action='index', id=None)) }</p>
    ${ h.end_form() }

<%def name="title()">
Social Network -
${ c.social_network.name } -
Edit -
 ${ parent.title() }
</%def>
