<%inherit file="/base.mako" />

<h2>${ c.person.fullname }</h2>
<p>Person ID: ${ c.person.id }</p>

%for fulfilment in c.person.fulfilments:
<%include file="view_fragment.mako" args="fulfilment=fulfilment" />
%endfor
