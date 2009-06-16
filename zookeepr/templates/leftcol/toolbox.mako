<%page args="toolbox_extra"/>
<%
    url = h.url_for()
    # Hack for schedule url
    if url.startswith('/schedule'):
        url = '/programme' + url
    mm = h.lca_menu

    where = ''
    if url == '' or url == '/':
        where = 'home'

    map = [(u, d) for (t, u, d) in mm]

    for (u, w) in map:
        if url.startswith('/' + w):
            where = w

    def cls(part):
        if part == where:
            return 'class="selected"'
        else:
            return 'class=""'
%>

## Toolbox links
        <div class = 'yellowbox'>
          <div class="boxheader">
            <h1>Toolbox</h1>
            <ul>
% if h.auth.authorized(h.auth.has_organiser_role):
              <li><em>Organiser</em></li>
              <li>${ h.link_to('Admin', url=h.url_for(controller='admin')) }</li>
              <li>${ h.link_to('New page', url=h.url_for(controller='db_content', action='new')) }</li>
%   if c.db_content and not h.url_for().endswith('/edit'):
             <li>${ h.link_to('Edit page', url=h.url_for(controller='db_content', action='edit', id=c.db_content.id)) }</li>
%   endif
% endif
${ toolbox_extra() }
% if h.signed_in_person():
             <li><em>${ h.signed_in_person().firstname }</em></li>
%   if h.lca_info["cfp_status"] == 'open':
             <li>${ h.link_to('Submit a paper', url=h.url_for(controller='proposal', action='new', id=None)) }</li>
%   endif
%   if h.lca_info["cfmini_status"] == 'open':
             <li>${ h.link_to('Submit a miniconf', url=h.url_for(controller='miniconf_proposal', action='new', id=None)) }</li>
%   endif
%   if len(h.signed_in_person().proposals) > 0:
             <li>${ h.link_to('My proposals', url=h.url_for(controller='proposal')) }</li>
%   endif
             <li>${ h.link_to('My profile', url=h.url_for(controller='person', action='view', id=h.signed_in_person().id)) }</li>
             <li> <a href="${h.url_for(controller='person', action='signout_confirm')}" ${ cls('login') |n}>Sign out</a></li>
% else:
             <li>${ h.link_to('Sign up', url=h.url_for(controller='person', action='new')) }</li>
             <li><a href="http://conf.linux.org.au/person/signin" ${ cls('login') |n}>Sign in</a></li>
% endif
            </ul>
% if h.signed_in_person():
            <p class = 'more'>${h.signed_in_person().email_address}</p>
% endif
          </div>
       </div>
