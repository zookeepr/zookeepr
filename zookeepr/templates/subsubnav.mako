<%
    # Provide the list of subsubmenus in here.
    submenus = c.subsubmenu
    url = h.url_for()
    # Hack for schedule url
    if url.startswith('/schedule'):
        url = '/programme' + url

    def cls(part):
        if part == url:
            return 'class="selected"'
        else:
            return 'class=""'

    def current(link):
        if url.startswith(link):
            return True
        else:
            return False

%>

  <!-- Tertiary navigation -->
  <ul id="tertiarynav">
%   for (link, name) in submenus:
    <li ${ cls(link) | n}><a href="${link}">${ name }</a></li>
%   endfor
  </ul>

