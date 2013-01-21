<%inherit file="/base.mako" />

    <h2>View Fulfilment</h2>
    <p><b>Person:</b> ${ c.fulfilment.person.fullname() }<br></p>
    <p><b>Person ID:</b> ${ c.fulfilment.person.id }<br></p>

<%include file="view_fragment.mako" args="fulfilment=c.fulfilment" />
