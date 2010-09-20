<%page args="miniconf_id, extra=''" />
<% miniconf = c.get_talk(miniconf_id) %>
<% speakers = [] %>
% if miniconf is not None:
%   for person in miniconf.people:
<%   speakers.append(person.firstname + ' ' + person.lastname) %>
%   endfor
%   if len(speakers) == 1: 
<%    speakers = speakers[0] %>
%   else: 
<%    speakers = '%s <i>and</i> %s' % (', '.join(speakers[: -1]), speakers[-1]) %>
%   endif
<% miniconf_url = h.url_for(controller='schedule', action='view_miniconf', id=miniconf.id) %>
<% teaser = h.make_teaser(h.truncate(miniconf.abstract, length=400)) %>
<% readmore = '' %>
%   if teaser[1] or len(miniconf.abstract) > 400:
<%   readmore = ' ' + h.link_to('read more', url=miniconf_url) %>
%   endif
% endif

% if miniconf is not None:
<i>${ h.link_to(miniconf.title, url=miniconf_url) }</i>
% else:
<i>Miniconf ${ miniconf_id } Not Found</i>
% endif
