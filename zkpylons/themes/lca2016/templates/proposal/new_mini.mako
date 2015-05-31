<%inherit file="/base.mako" />

<h1>Submit a Miniconf</h1>
<p class="lead">Please read the <a href="${ h.url_for("/programme/miniconfs") }">Miniconf Info</a> page before submitting a proposal.</p>

<form action="/programme/submit_a_miniconf" method="post" data-toggle="validator" class="form-horizontal" enctype="multipart/form-data">

<%include file="form_mini.mako" args="editing=False" />

  <div class="form-group">
    <button type="submit" class="btn btn-primary">Submit miniconf proposal</button>
  </div>
${ h.end_form() }

<%def name="short_title()"><%
  return "Submit a Miniconf"
%></%def>
<%def name="title()" >
Submit a Miniconf - ${ parent.title() }
</%def>

