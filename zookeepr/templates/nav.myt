<div id="navcontainer">
    <ul id="navlist">
        <li><a href="/" <%cls('home')%> >Home</a></li>
        <li><a href="/about" <% cls('about') %>>About</a></li>
        <li><a href="/sponsors" <% cls('sponsors') %>>Sponsors</a></li>
        <li><a href="/media" <% cls('media') %>>Media</a></li>
        <li><a href="/mini-confs" <% cls('mini-confs') %>>Mini-confs</a></li>
        <li><a href="/contact" <% cls('contact') %>>Contact</a></li>
% if 'signed_in_person_id' not in session:
        <li><a href="<% h.url(controller='account', action='signin', id=None)() %>" <% cls('login') %>>login / register</a></li>
% else:
        <li><a href="<% h.url(controller='account', action='signout', id=None)() %>" <% cls('login') %>>logout</a></li>
% #endif
    </ul>
</div>
% if submenus.has_key(where):
<div id="youarehere">
  <ul id="sub">
%   for sub in submenus[where]:
%     url = where+'/'+sub
%     if url==c.url:
        <li class="now"><% sub %>
%     else:
        <li><a href="/<%url%>"><% sub %></a>
%     #endif
%   #endif
  </ul>
</div>
% #endif

<%init>
# The current URL can be accessed as h.url()()
url = h.url()()

where = 'home'
map = (
  ('/about', 'about'),
  ('/sponsors', 'sponsors'),
  ('/media', 'media'),
  ('/mini-confs', 'mini-confs'),
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

submenus = {
  'about': ('history', 'melbourne', 'linux', 'floss', 'credits'),
}
</%init>

