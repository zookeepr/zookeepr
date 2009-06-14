<%inherit file="/base.mako" />
<h2>Edit proposal "${ c.proposal.title }"</h2>

<div id="proposal">

% if c.paper_editing == 'closed':
<p>Editing has been disabled while proposals are reviewed. If your paper is successful in its submission, you will be able to update your details later when the schedule is finalised.</p>
% else:

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

% endif
</div>

