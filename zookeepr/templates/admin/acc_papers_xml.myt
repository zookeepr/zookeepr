<talks>
% publish = True
% record = True
% yesno = {True: 'yes', False: 'no', None: 'unknown'}
% for t in c.talks:
  <talk id="<% t.id %>">
    <title><% t.title |h%></title>
%   speakers = [(s.lastname.lower(), s.firstname.lower(), s) for s in t.people]
%   speakers.sort()
%   for sortkey_1, sortkey_2, s in speakers:
%     if record:
%       record = s.registration.speaker_record
%     if publish:
%       publish = s.registration.speaker_video_release
    <speaker id="<% s.id %>"><% s.firstname |h%> <% s.lastname |h%></speaker>
%   #endfor
    <record><% yesno[record] %></record>
    <publish><% yesno[publish] %></publish>
  </talk>
% #endfor
</talks>
