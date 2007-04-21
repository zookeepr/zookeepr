% if submenus.has_key(where):
<div id="youarehere">
  <ul id="sub">
%   for sub in submenus[where]:
%     link = '/'+where+'/'+sub
%     link = link.replace(' ', '_')
%     if link==url:
        <li class="now"><% sub %></li>
%     else:
        <li><a href="<%link%>"><% sub %></a></li>
%     #endif
%   #endfor
  </ul>
</div>
% #endif

<%init>
# Edit the list of submenus here :-)
submenus = {
  'about': ('history', 'melbourne', 'linux', 'floss', 'credits'),
  'mini-confs': ('submit mini-conf proposal',),
}

# The current URL can be accessed as h.url()()
url = h.url()()

where = 'home'
map = (
  ('/about', 'about'),
  ('/sponsors', 'sponsors'),
  ('/media', 'media'),
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

