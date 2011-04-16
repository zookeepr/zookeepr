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

        <ul class="netv-menu" style="background: #53761f !important">

%   for sub in submenus[where]:
<%
     link = sub.replace('/', '_').lower()
     link = '/'+where+'/'+link
     link = link.replace(' ', '_')
%>
%     if current(link):
            <li class="selected" style="background: #99ff33 !important"><a href=""><span class="l"></span><span class="r"></span><span class="t">${ sub }</span></a></li>
%     else:
            <li><a href="${ link }"><span class="l"></span><span class="r"></span><span class="t">${ sub }</span></a></li>
%     endif
%   endfor
       </ul>
    </div>
% endif
