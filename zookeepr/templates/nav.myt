<div id="navcontainer">
    <ul id="navlist">
        <li><a href="/" <%cls('home')%> >Home</a></li>
        <li><a href="/about" <% cls('about') %>>About</a></li>
        <li><a href="/sponsors-media" <% cls('sponsors-media') %>>Sponsors / Media</a></li>
        <li><a href="/mini-confs" <% cls('mini-confs') %>>Mini-confs</a></li>
        <li><a href="/contact" <% cls('contact') %>>Contact</a></li>
% if 'signed_in_person_id' not in session:
        <li><a href="<% h.url(controller='account', action='signin', id=None)() %>" <% cls('login') %>>login / register</a></li>
% else:
        <li><a href="<% h.url(controller='account', action='signout', id=None)() %>" <% cls('login') %>>logout</a></li>
% #endif
    </ul>
</div>

<%init>
# The current URL can be accessed as h.url()()
url = h.url()()

where = 'home'
map = (
  ('/about', 'about'),
  ('/sponsors-media', 'sponsors-media'),
  ('/mini-confs', 'mini-confs'),
  ('/cfp', 'mini-confs'),
  ('/contact', 'contact'),
  ('/account', 'login'),
  ('/error', ''),
)

for (u, w) in map:
  if url.startswith(u):
    where = w

def cls(part):
  if part==where:
    return 'class="now"'
  else:
    return 'class=""'
</%init>

