<%
    # The current URL can be accessed as h.url()()
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
            return 'class="now"'
        else:
            return 'class=""'
%>


      <ul class="main_menu">
% for (t, u, c) in mm:
        <li><a href="${u}" ${cls(c)}>${t}</a></li>
% endfor
% if h.signed_in():
        <li><a href="${h.url_for(controller='person', action='signout_confirm')}" ${ cls('login') }>Sign out</a> (${h.signed_in()})</li>
% else:
        <li><a href="${h.url_for(controller='person', action='signin')}" ${ cls('login') }>Sign in</a></li>
% endif
      </ul>

