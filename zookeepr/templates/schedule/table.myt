<h2>Schedule</h2>

% for (day, programme) in c.programme.items():
    <h3><% day %></h3>
%   for (building, items) in programme.items():
%       for (theatre, talks) in items.items():
%           for talk in talks:
                <p><% building %> <% theatre %>: <% talk.scheduled %> -> <% talk.finished %> - <% talk.title %></p>
%           #endfor
%       #endfor
%   #endfor
% #endfor

<%method title>
Programme - <& PARENT:title &>
</%method>
