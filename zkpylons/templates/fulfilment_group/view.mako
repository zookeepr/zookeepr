<%inherit file="/base.mako" />

%if c.fulfilment_group.person:
<h2>${ c.fulfilment_group.person.fullname }</h2>
<p>Person ID: ${ c.fulfilment_group.person_id }</p>
%endif

%for fulfilment in c.fulfilment_group.fulfilments:
<%include file="/fulfilment/view_fragment.mako" args="fulfilment=fulfilment" />
%endfor
