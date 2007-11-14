<talks>
% for t in c.talks:
  <talk id="<% t.id %>">
    <title><% t.title |h%></title>
%   speakers = [(s.lastname.lower(), s.firstname.lower(), s) for s in t.people]
%   speakers.sort()
%   for sortkey_1, sortkey_2, s in speakers:
    <speaker id="<% s.id %>"><% s.firstname |h%> <% s.lastname |h%></speaker>
%   #endfor
  </talk>
% #endfor
</talks>
