<%inherit file="/base.mako" />
<% c.signed_in_person = h.signed_in_person() %>
<%def name="toolbox_extra()">
% if h.auth.authorized(h.auth.has_organiser_role) or c.funding_editing == 'open' and c.signed_in_person == c.funding.person:
  <li>${ h.link_to('Edit Funding Application', url=h.url_for(controller='funding', action='edit',id=c.funding.id)) }</li>
% endif 
</%def>

<%def name="heading()">
  ${ c.funding.type.name }
</%def>

<% c.signed_in_person = h.signed_in_person() %>

<h2>${ self.heading() }</h2>


<%include file="view_fragment.mako" />


${ next.body() }

<hr>
% if h.auth.authorized(h.auth.has_organiser_role) or c.funding_editing == 'open' and c.signed_in_person == c.funding.person:
  <li>${ h.link_to('Edit Funding Application', url=h.url_for(controller='funding', action='edit',id=c.funding.id)) }</li>
% endif 
