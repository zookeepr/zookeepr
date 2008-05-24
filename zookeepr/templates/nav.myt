    <ul class="main_menu">

% for (t, u, c) in mm:
        <li><a href="<% u %>" <% cls(c) %>><% t %></a></li>
% #endfor

% if 'signed_in_person_id' in session:
        <li><a href="<% h.url(controller='account', action='signin', id=None)() %>" <% cls('login') %>>Sign in</a></li>
% else:
        <li><a href="<% h.url(controller='account', action='signout', id=None)() %>" <% cls('login') %>>Sign out</a></li>
% #endif
    </ul>


<%init>
# The current URL can be accessed as h.url()()
url = h.url()()

mm = h.lca_menu

where = ''

map = [(u, c) for (t, u, c) in mm]

for (u, w) in map:
  if url.startswith('/' + w):
    where = w

def cls(part):
  if part==where:
    return 'class="now"'
  else:
    return 'class=""'
</%init>
