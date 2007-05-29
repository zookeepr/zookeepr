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
  'sponsors-media': ('sponsorship packages','media coverage',),
  'mini-confs': ('submit mini-conf proposal',),
  'papers': ('submit a paper', 'speaker FAQ'),
}

# The current URL can be accessed as h.url()()
url = h.url()()

where = 'home'
map = (
  ('/about', 'about'),
  ('/sponsors-media', 'sponsors-media'),
  ('/mini-confs', 'mini-confs'),
  ('/cfp', 'mini-confs'),
  ('/papers', 'papers'),
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

