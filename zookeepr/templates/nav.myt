<div id="navcontainer">
    <ul id="navlist">
      <!--
        <li><a href="/" <%cls('home')%> >Home</a></li>
        <li><a href="/2008/about" <% cls('about') %>>About</a></li>
        <li><a href="/2008/sponsors-media" <% cls('sponsors-media') %>>Sponsors / Media</a></li>
        <li><a href="/mini-confs" <% cls('mini-confs') %>>Mini-confs</a></li>
        <li><a href="/presentations" <% cls('presentations') %>>Presentations</a></li>
        <li><a href="/2008/contact" <% cls('contact') %>>Contact</a></li>
      -->

% for (t, u, c) in mm:
        <li><a href="<% u %>" <% cls(c) %>><% t %></a></li>
% #endfor

% if 'signed_in_person_id' not in session:
        <li><a href="<% h.url(controller='account', action='signin', id=None)() %>" <% cls('login') %>>sign in</a></li>
% else:
        <li><a href="<% h.url(controller='account', action='signout', id=None)() %>" <% cls('login') %>>sign out</a></li>
% #endif
    </ul>
</div>

<%init>
# The current URL can be accessed as h.url()()
url = h.url()()

where = 'home'
map = [
  ('/2008/about', 'about'),
  ('/2008/sponsors-media', 'sponsors-media'),
  ('/mini-confs', 'mini-confs'),
  ('/cfp', 'mini-confs'),
  ('/papers', 'presentations'),
  ('/presentations', 'presentations'),
  ('/registration', 'register'),
  ('/proposal', 'programme'),
  ('/invoice', 'register'),
  ('/2008/contact', 'contact'),
  ('/account', 'login'),
  ('/error', ''),
]

# Import the navbar from Matrix ("mm" stands for "matrix menu")
import re, urllib
mm = 'http://matrix.mel8ourne.org/_designs/zookeepr-files/menu-list'
mm = urllib.urlopen(mm).readlines()
# mm = []
mm = [mme.split(',', 2) for mme in mm]
mm = [(t.strip(' \t"'), re.sub('^http://[^/]*/', '/', u.strip(' \t\n"')))
							  for (t, u) in mm]
mm = [(t, u, u.split('/')[1]) for (t, u) in mm if u!='/account/signin']

map = map + [(u, c) for (t, u, c) in mm]

for (u, w) in map:
  if url.startswith(u):
    where = w

def cls(part):
  if part==where:
    return 'class="now"'
  else:
    return 'class=""'
</%init>
