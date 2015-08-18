<Div id="proposal">

<p class="submitted">
Proposal for a
${ c.proposal.type.name } 
submitted by
% for p in c.proposal.people:
${ p.firstname } ${ p.lastname }
&lt;${ p.email_address }&gt;
% endfor
at
${ c.proposal.creation_timestamp.strftime("%Y-%m-%d&nbsp;%H:%M") | n}<br />
(last updated at ${ c.proposal.last_modification_timestamp.strftime("%Y-%m-%d&nbsp;%H:%M") | n})
</p>

% if c.proposal.type.name:
<p class="url">
<em>Proposal Type:</em>
${ c.proposal.type.name }
</p>
% endif

<div class="abstract">
<p>
<em>Abstract:</em>
</p>
<blockquote>
<p>${ h.line_break(h.util.html_escape(c.proposal.abstract)) | n}</p>
</blockquote>
</div>

<div class="private_abstract">
<p>
<em>Private Abstract:</em>
</p>
<blockquote>
<p>${ h.line_break(h.util.html_escape(c.proposal.private_abstract)) | n}</p>
</blockquote>
</div>

% if c.proposal.technical_requirements:
<div class="technical_requirements">
<p>
<em>Technical Requirements:</em>
</p>
<blockquote>
<p>${ h.line_break(h.util.html_escape(c.proposal.technical_requirements)) | n}</p>
</blockquote>
</div>
% endif

% if c.proposal.audience.name:
<p class="url">
<em>Target Audience:</em>
${ c.proposal.audience.name }
</p>
% endif


% if c.proposal.project:
<p class="url">
<em>Project:</em>
${ c.proposal.project | h }
</p>
% endif

% if c.proposal.url:
<p class="url">
<em>URL:</em>
## FIXME: I reckon this should go into the helpers logic
%   if '://' in c.proposal.url:
<a href="${ c.proposal.url | h }">${ c.proposal.url | h }</a>
%   else:
<a href="http://${ c.proposal.url | h }">${ c.proposal.url | h }</a>
%   endif
</p>
% endif

% if c.proposal.abstract_video_url:
<p class="video">
<em>Video Abstract:</em>
## FIXME: I reckon this should go into the helpers logic
%   if '://' in c.proposal.abstract_video_url:
<a href="${ c.proposal.abstract_video_url | h }">${ c.proposal.abstract_video_url | h }</a>
%   else:
<a href="http://${ c.proposal.abstract_video_url | h }">${ c.proposal.abstract_video_url | h }</a>
%   endif
</p>
% endif

% for person in c.proposal.people:
<h2>${ person.firstname | h} ${ person.lastname | h}</h2>
%   if h.url_for().endswith('review') is True and ('reviewer' in [x.name for x in c.signed_in_person.roles]) or ('organiser' in [x.name for x in c.signed_in_person.roles]):
<p class="submitted">
${ person.firstname | h } ${ person.lastname | h } &lt;${ person.email_address }&gt;
%if person.url is not None and len(person.url) > 0:
<a href="${ person.url}">Speaker's Homepage</a>
%endif
<br>
${ h.link_to('(view details)', url=h.url_for(controller='person', action='view', id=person.id)) }
${ h.link_to('(stalk on Google)', url='http://google.com/search?q=%s+%s' % (person.fullname, person.email_address)) }
${ h.link_to('(linux specific stalk)', url='http://google.com/linux?q=%s+%s' % (person.fullname, person.email_address)) }
${ h.link_to('(email address only stalk)', url='http://google.com/search?q=%s' % person.email_address) }
</p>
%   endif
<div class="bio">
<p>
<em>Bio:</em>
</p>
<blockquote><p>
%   if person.bio:
${ h.line_break(h.util.html_escape(person.bio)) |n}
%   else:
[none provided]
%   endif
</p></blockquote>
</div>

<div class="experience">
<p>
<em>Experience:</em>
</p>
<blockquote><p>
%   if person.experience:
${ h.line_break(h.util.html_escape(person.experience)) |n}
%   else:
[none provided]
%   endif
</p></blockquote>
</div>
% endfor
<p></p>
<div class="attachment">
<p><em>Attachments:</em></p>
% if len(c.proposal.attachments) > 0:
<table>
<tr>
<th>Filename</th>
<th>Size</th>
<th>Date uploaded</th>
<th>&nbsp;</th>
</tr>
% endif

% for a in c.proposal.attachments:
<tr class="${ h.cycle('even', 'odd') }">

<td>
${ h.link_to(h.util.html_escape(a.filename), url=h.url_for(controller='attachment', action='view', id=a.id)) }
</td>

<td>
%if len(a.content) >= (1024*1024):
${ round(len(a.content)/1024.0/1024.0, 1) } MB
%elif len(a.content) >= (1024):
${ round(len(a.content)/1024.0, 1) } kB
%else:
${ len(a.content) } B
%endif
</td>

<td>
${ a.creation_timestamp.strftime("%Y-%m-%d %H:%M") }
</td>

<td>
${ h.link_to('delete', url=h.url_for(controller='attachment', action='delete', id=a.id)) }
</tr>
% endfor

% if len(c.proposal.attachments) > 0:
</table>
% endif
% if c.signed_in_person in c.proposal.people or ('organiser' in [x.name for x in c.signed_in_person.roles]):
<p>
${ h.link_to('Add an attachment', url=h.url_for(action='attach')) }
</p>
% endif
</div>

% if c.cfp_hide_assistance_info == 'no':
    % if c.proposal.accommodation_assistance:
<p>
    <em>Accommodation assistance:</em> ${ c.proposal.accommodation_assistance.name }</p>
    % endif

    % if c.proposal.travel_assistance:
<p>
    <em>Travel assistance:</em> ${ c.proposal.travel_assistance.name }</p>
    % endif
% endif

<p><em>Consents:</em><blockquote>
<p>I allow ${ c.config.get("event_parent_organisation") } to record my talk.</p>

<p>${ allow(c.proposal.video_release) } ${ c.config.get("event_parent_organisation") } to release any
recordings of my presentations, tutorials and minconfs under the <a href="${ c.config.get("media_license_url") }">${ c.config.get("media_license_name") }</a></p>

<p>${ allow(c.proposal.slides_release) } ${ c.config.get("event_parent_organisation") } to release any other material (such as slides) from my presentations, tutorials and minconfs under the <a href="${ c.config.get("media_license_url") }">${ c.config.get("media_license_name") }</a>
</p>


% if c.proposal.video_release or c.proposal.slides_release:
<p>I confirm that I have the authority to allow
${ c.config.get("event_parent_organisation") } to release the above material.
i.e., if your talk includes any information about your employer, or another
persons copyrighted material, that person has given you authority to
release this information.</p>
% endif

% if not c.proposal.video_release or not c.proposal.slides_release:
<p>Please consider allowing us to share both the video of your talk and your
slides, so that the community can gain the maximum benefit from your
talk!</p>
% endif
</blockquote>
<hr>
</div>

<%def name="title()">
${ h.truncate(c.proposal.title) } - ${ c.proposal.type.name } proposal - ${ parent.title() }
</%def>
<%def name="allow(b)">
<%
    if b:
        return 'I allow'
    else:
        return 'I DO NOT allow'
%>
</%def>
