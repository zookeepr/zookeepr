<%
    url = h.url_for()
    # Hack for schedule url
    if url.startswith('/schedule'):
        url = '/programme' + url
    mm = h.lca_menu

    where = ''
    if url == '' or url == '/':
        where = 'home'

    map = [(u, c) for (t, u, c) in mm]

    for (u, w) in map:
        if url.startswith('/' + w):
            where = w

    def cls(part):
        if part == where:
            return 'class="selected"'
        else:
            return 'class=""'
%>

      <ul class="netv-menu">
% for (t, u, c) in mm:
%   if c == 'selected':
          <li>${ t |n }</li>
%   else:
          <li ${ cls(c) |n}><a href="${ u }"><span class="l"></span><span class="r"></span><span class="t">${ t }</span></a></li>
%   endif

% endfor
      </ul>

<%
    # Edit the list of submenus here :-)
    submenus = h.lca_submenus

    # The current URL can be accessed as h.url()()
    url = h.url_for()
    # Hack for schedule url
    if url.startswith('/schedule'):
        url = '/programme' + url

    where = ''
    map = h.lca_menu

    for (t, u, w) in map:
        if url.startswith('/' + w):
            where = w

    def cls(part):
        if part == where:
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
  <!-- Secondary navigation -->
  <div class="netv-nav">
	  <div class="l"></div>
      <div class="r"></div>

        <ul class="netv-menu">
%   for sub in submenus[where]:
<%
     link = sub.replace('/', '_').lower()
     link = '/'+where+'/'+link
     link = link.replace(' ', '_')
%>
%     if current(link):
            <li ${ cls(c) |n}><a href="${ link }"><span class="l"></span><span class="r"></span><span class="t">${ sub }</span></a></li>
%     else:
            <li ${ cls(c) |n}><a href="${ link }"><span class="l"></span><span class="r"></span><span class="t">${ sub }</span></a></li>
%     endif
%   endfor
       </ul>
    </div>
% endif

