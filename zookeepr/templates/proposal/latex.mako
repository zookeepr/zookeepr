% for type in c.proposal_type:
%   if type.name != 'Miniconf' and type.name != 'Keynote':
<%
      talks_by_person = dict()
      for t in type.proposals:
        if t.status.name == 'Accepted' and t.scheduled is not None:
          lastname = t.people[0].lastname
          if lastname not in talks_by_person:
            talks_by_person[lastname] = dict()

          if t.people[0].fullname() not in talks_by_person[lastname]:
            talks_by_person[lastname][t.people[0].fullname()] = []

          talks_by_person[lastname][t.people[0].fullname()].append(t)
%>

%     if len(talks_by_person) > 0:
\lcasection{${ type.name }}
<%
  lastnames = talks_by_person.keys()
  lastnames.sort()
%>
%       for lastname in lastnames:
<%
  names = talks_by_person[lastname].keys()
  names.sort()
%>
%         for name in names:
%           for t in talks_by_person[lastname][name]:
<%
  presenters = []
  for person in t.people:
    presenters.append(person.fullname())
%>
\abstract{${ ",".join(presenters) }}{${ t.title }}{${ t.scheduled.strftime("%A %H:%M") } - ${ t.building } - ${ t.theatre }}

${ h.latex_clean(t.abstract) | n }

%           endfor
%         endfor
%       endfor
%     endif
%   endif
% endfor
