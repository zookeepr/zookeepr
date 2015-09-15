<%inherit file="/base.mako" />

    <h2>New product category</h2>


    <form action="/product_category/new" method="post" data-toggle="validator">
    
<%include file="form.mako" />
      <p>${ h.submit('button', "New") }
      ${ h.link_to('Back', url=h.url_for(action='index')) }</p>
    ${ h.end_form() }
