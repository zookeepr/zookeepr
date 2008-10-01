% talk = c.get_talk(talk_id)
% speakers = []
% for person in talk.people:
%   speakers.append(h.esc(person.firstname + ' ' + person.lastname))
% #endfor
% if len(speakers) == 1: 
%    speakers = speakers[0]
% else: 
%    speakers = '%s <i>and</i> %s' % (', '.join(speakers[: -1]), speakers[-1])
% #endif

<p class="talk_title"><% h.link_to(h.esc(talk.title), url=h.url(controller='schedule', action='view_talk', id=talk.id)) %> <i>by</i> <span class="by_speaker"><% speakers %></span></p>

<%args>
talk_id
</%args>
