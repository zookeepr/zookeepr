<%
# Edit the list of submenus here :-)
submenus = h.lca_submenus

# The current URL can be accessed as h.url_for()()
url = h.url_for()
# Hack for schedule url
if url.startswith('/schedule'): url = '/programme' + url
where = ''
map = h.lca_menu

for (t, u, w) in map:
  if url.startswith('/' + w):
    where = w

def cls(part):
  if part==where:
    return 'class="now"'
  else:
    return 'class=""'

def current(link):
  if url.startswith(link):
    return True
  else:
    return False

%>

% if submenus.has_key(where):
  <div class="yellowbox">
    <div class="boxheader">
      <ul>
%   for sub in submenus[where]:
<%
     link = sub.replace('/', '_').lower()
     link = '/'+where+'/'+link
     link = link.replace(' ', '_')
%>
%     if current(link):
        <li><a href="${ link }" class="selected">${ sub }</a></li>
%     else:
        <li><a href="${ link }">${ sub }</a></li>
%     endif
%   endfor
      </ul>
    </div>
  </div>
% endif

  <!-- Sponsors on left column -->
  <div class="whitebox">
    <div class="boxheader">
      <h1>Our Emperor Sponsors</h1>
      <ul>
        <li><a href="http://www.internetnz.org.nz"><img src="/sponsors/InternetNZ.png" alt="InternetNZ" title="Internet NZ works to keep the Internet open and uncaptureable, protecting and promoting the Internet for New Zealand." /></a></li>
      </ul>
    </div>
  </div>



