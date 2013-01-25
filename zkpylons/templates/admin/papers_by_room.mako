<%inherit file="/base.mako" />

<% theatre = '' %>
% for p in c.proposals:
%   if p.theatre != theatre:
<%     theatre = p.theatre %>
<%     day = '' %>
  <h1>${ p.theatre }</h1>
%   endif

%   if p.scheduled is None:
Huh? No scheduled time for talk ${ p.id }.
%   else:
%     if day != p.scheduled.strftime('%Y-%m-%d - %A'):
<%      day = p.scheduled.strftime('%Y-%m-%d - %A') %>
<h2>${ day }</h2>
%     endif
<h3>${ p.scheduled.strftime('%H:%M') } - ${ p.title }</h3>

<p>${ h.line_break(h.url_to_link(p.abstract)) | n}</p>

%     for person in p.people:
<h4>${ person.fullname }</h2>
<div class="bio">
<p>
%        if person.bio:
${ h.line_break(h.url_to_link(person.bio)) | n  }
%        else:
[no bio provided]
%        endif
</p>
</div>
%     endfor
%   endif

% endfor
