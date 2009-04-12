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


      <ul id="primarynav">
% for (t, u, c) in mm:
%   if c == 'selected':
          <li>${ t |n }</li>
%   else:
          <li ${ cls(c) |n}><a href="${ u }">${ t }</a></li>
%   endif

% endfor
% if h.signed_in_person():
        <li><a href="${h.url_for(controller='person', action='signout_confirm')}" ${ cls('login') |n}>Sign out</a> (${h.signed_in_person().email_address})</li>
% else:
        <li><a href="${h.url_for(controller='person', action='signin')}" ${ cls('login') |n}>Sign in</a></li>
% endif
      </ul>

