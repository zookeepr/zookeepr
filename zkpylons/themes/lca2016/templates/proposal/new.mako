<%inherit file="/base.mako" />

<h1>Submit a Proposal</h1>
<p class="lead">Please read the <a href="${ h.url_for("/cfp") }">Call for Proposals</a> page before submitting a proposal.</p>

<form action="/proposal/new" method="post" data-toggle="validator" class="form-horizontal" enctype="multipart/form-data">

<%include file="form.mako" args="editing=False" />

  <div class="form-group">
    <button type="submit" class="btn btn-primary">Submit talk proposal</button>
  </div>
${ h.end_form() }

<%def name="short_title()"><%
  return "Submit a Proposal"
%></%def>
<%def name="title()" >
Submit a Paper - ${ parent.title() }
</%def>
