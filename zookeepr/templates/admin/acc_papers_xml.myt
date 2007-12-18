<talks>
% for t in c.talks:
  <talk id="<% t.id %>">
    <title><% t.title |h%></title>
%   publish = []
%   record = []
%   speakers = [(s.lastname.lower(), s.firstname.lower(), s) for s in t.people]
%   speakers.sort()
%   for sortkey_1, sortkey_2, s in speakers:
%     if s.registration:
%       record.append(s.registration.speaker_record)
%       publish.append(s.registration.speaker_video_release)
%     else:
%       record.append(None)
%       publish.append(None)
%     #endif
    <speaker id="<% s.id %>"><% s.firstname |h%> <% s.lastname |h%></speaker>
%   #endfor
    <record><% yesno(record) %></record>
    <publish><% yesno(publish) %></publish>
  </talk>
% #endfor
</talks>
<%init>
def yesno(list):
  if False in list:
    return 'no'
  elif None in list:
    return 'unknown'
  else:
    return 'yes'
</%init>
