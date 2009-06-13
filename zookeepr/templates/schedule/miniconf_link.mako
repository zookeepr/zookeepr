<% miniconf = c.get_talk(miniconf_id) %>
<% speakers = [] %>
% for person in miniconf.people:
<%   speakers.append(person.firstname + ' ' + person.lastname) %>
% endfor
% if len(speakers) == 1: 
<%    speakers = speakers[0] %>
% else: 
<%    speakers = '%s <i>and</i> %s' % (', '.join(speakers[: -1]), speakers[-1]) %>
% endif
<% miniconf_url = h.url(controller='schedule', action='view_miniconf', id=miniconf.id) %>
<% teaser = h.make_teaser(h.truncate(miniconf.abstract, length=400)) %>
<% readmore = '' %>
% if teaser[1] or len(miniconf.abstract) > 400:
<%   readmore = ' ' + h.link_to('read more', url=miniconf_url) %>
% endif

<a name="${ day }_${ h.computer_title(miniconf.title) }"></a>
<h3>${ h.link_to(miniconf.title, url=miniconf_url) }</h3>
<blockquote>
<p>${ h.line_break(h.url_to_link(teaser[0])) }${ readmore }</p>
</blockquote>
