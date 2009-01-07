      <ul id="primarynav">
% for (t, u, c) in mm:
%	if c == 'selected':
          <li><% t %></li>
%        else:
          <li <% cls(c) %>><a href="<% u %>"><% t %></a></li>
%        #endif
% #endfor
% if 'signed_in_person_id' in session:
        <li><a href="<% h.url(controller='person', action='signout', id=None)() %>" <% cls('login') %>>Sign out</a></li>
% else:
        <li><a href="<% h.url(controller='person', action='signin', id=None)() %>" <% cls('login') %>>Sign in</a></li>
% #endif
      </ul>

<%init>
# The current URL can be accessed as h.url()()
url = h.url()()
# Hack for schedule url
if url.startswith('/schedule'): url = '/programme' + url
mm = h.lca_menu

where = ''
if url == '' or url == '/':
    where = 'home'

map = [(u, c) for (t, u, c) in mm]

for (u, w) in map:
  if url.startswith('/' + w):
    where = w

def cls(part):
  if part==where:
    return 'class="selected"'
  else:
    return 'class=""'
</%init>
