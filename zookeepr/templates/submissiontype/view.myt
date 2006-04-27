<%flags>
	inherit="/layout.myt"
</%flags>

View submission type

% for (label, key) in [('Name', 'name')]:
<div class="formlabel"><% label %>:</div>
<div class="formfield"><% getattr(c.submissiontype, key) %></div>
% #endfor
