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
  '2008/about': ('history', 'melbourne', 'linux', 'floss', 'credits'),
  '2008/sponsors-media': ('sponsorship packages','media coverage',),
  'mini-confs': ('submit mini-conf proposal', 'mini-conf organiser FAQ'),
  'papers': ('submit a presentation', 'speaker FAQ', 'sample form'),
  'presentations': ('submit a presentation', 'speaker FAQ', 'sample form'),
}

# The current URL can be accessed as h.url()()
url = h.url()()

where = 'home'
map = (
  ('/2008/about', '2008/about'),
  ('/2008/sponsors-media', '2008/sponsors-media'),
  ('/mini-confs', 'mini-confs'),
  ('/cfp', 'mini-confs'),
  ('/papers', 'presentations'),
  ('/presentations', 'presentations'),
  ('/2008/contact', '2008/contact'),
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

