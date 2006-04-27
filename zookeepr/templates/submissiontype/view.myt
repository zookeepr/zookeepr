<%flags>
	inherit="/layout.myt"
</%flags>

View submission type

(<a href="<% h.url_for(action='new') %>">new stype</a>)
(<a href="<% h.url_for(action='index') %>">list stypes</a>)

(<a href="<% h.url_for(action='edit') %>">edit this stype</a>)
(<a href="<% h.url_for(action='delete') %>">delete this stype</a>)


% for (label, key) in [('Name', 'name')]:
<div class="formlabel"><% label %>:</div>
<div class="formfield"><% getattr(c.submissiontype, key) %></div>
% #endfor
