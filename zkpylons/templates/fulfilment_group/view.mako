<%inherit file="/base.mako" />

%if c.fulfilment_group.person:
<h2>Fulfilment Group - ${ c.fulfilment_group.id }</h2>
<p><b>Person:</b> ${ h.link_to(c.fulfilment_group.person.fullname, h.url_for(controller='person', action='view', id=c.fulfilment_group.person_id)) }</p>
%endif
<p><b>Code:</b> ${ c.fulfilment_group.code }</p>

%for fulfilment in c.fulfilment_group.fulfilments:
<%include file="/fulfilment/view_fragment.mako" args="fulfilment=fulfilment" />
%endfor
