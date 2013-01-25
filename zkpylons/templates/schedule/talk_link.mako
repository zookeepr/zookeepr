<%page args="talk_id, extra=''" />
<% talk = c.get_talk(talk_id) %>
<% speakers = [] %>
% if talk is not None:
%   for person in talk.people:
<%   speakers.append(h.escape(person.fullname)) %>
%   endfor
%   if len(speakers) == 1:
<%    speakers = speakers[0] %>
%   else:
<%    speakers = '%s <i>and</i> %s' % (', '.join(speakers[: -1]), speakers[-1]) %>
%   endif
% endif

<% resources = '' %>
<% slides_videos = [] %>
% if c.slide_list.has_key(str(talk_id)):
<%   slides_videos.append('<a href="' + c.download_path + '/' + c.slide_list[str(talk_id)] + '">Slides</a>') %>
% endif
% if c.ogg_list.has_key(str(talk_id)):
<%   slides_videos.append('<a href="' + c.ogg_path + '/' + c.ogg_list[str(talk_id)] + '">OGG</a>') %>
% endif
% if c.speex_list.has_key(str(talk_id)):
<%   slides_videos.append('<a href="' + c.speex_path + '/' + c.speex_list[str(talk_id)] + '">SPEEX</a>') %>
% endif
% if len(slides_videos) > 0:
<%   resources = '<br>[' + (",".join(slides_videos)) + ']' %>
% endif

<div class="programmeTalkId">${ talk_id }</div>
<p class="talk_title">
% if talk is not None:
    ${ h.link_to(talk.title, url=h.url_for(controller='schedule', action='view_talk', id=talk.id)) }${ extra } <i>by</i> <span class="by_speaker">${ speakers | n }</span>
% else:
    <span class="error-message">Talk ${ talk_id } not found</span>
% endif
<span style="text-align: center; font-size: smaller; font-style: oblique;">${ resources |n }</span></p>
