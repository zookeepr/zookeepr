<%inherit file="/base.mako" />
<h2>Edit proposal "${ c.proposal.title }"</h2>

<div id="proposal">

${ h.form(h.url_for()) }
%   if c.miniconf:
        <%include file="form_mini.mako" args="editing=True" />
%   else:
        <%include file="form.mako" args="editing=True" />
%   endif

<p class="submit">
${ h.submit('Update', 'Update') }
</p>

${ h.end_form() }

</div>

