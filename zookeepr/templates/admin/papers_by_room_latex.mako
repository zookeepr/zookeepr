<% theatre = '' %>
% for p in c.papers:
%   if p.theatre != theatre:
<%     theatre = p.theatre %>
<%     day = '' %>
\lcasection{${ p.theatre }}
%   endif

%   if p.scheduled is None:
Huh? No scheduled time for talk ${ p.id }.
%   else:
%     if day != p.scheduled.strftime('%Y-%m-%d - %A'):
<%      day = p.scheduled.strftime('%Y-%m-%d - %A') %>
\lcasubsection{${ day }}
%     endif
\lcasubsubsection{${ p.scheduled.strftime('%H:%M') } - ${ p.title }}

${ h.latex_clean(p.abstract) | n}

%     for person in p.people:
{\bf ${ person.fullname() }}

%        if person.bio:
${ h.latex_clean(person.bio) | n  }
%        else:
[no bio provided]
%        endif
%     endfor
%   endif

% endfor
