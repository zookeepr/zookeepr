<%inherit file="base.mako" />

<ul>
% for (t, u, c) in h.lca_menu:
  <li> <a href="${ u }">${ t }</a></li>
%   if h.lca_submenus.has_key(c):
  <ul>
%     for sub in h.lca_submenus[c]:
<%
     link = sub.replace('/', '_').lower()
     link = '/' + c + '/' + link
     link = link.replace(' ', '_')
%>
    <li> <a href="${ link }">${ sub }</a></li>
%     endfor
  </ul>
%   endif
% endfor
  <li>Person</li>
  <ul>
    <li> <a href="/person/new">New Account</a></li>
    <li> <a href="/person/signin">Sign In</a></li>
    <li> <a href="/person/signout">Sign Out</a></li>
% if h.signed_in_person():
    <li>${ h.link_to('My profile', h.url_for(controller='person', action='view', id=h.signed_in_person().id)) }</li>
% endif
  </ul>
</ul>

