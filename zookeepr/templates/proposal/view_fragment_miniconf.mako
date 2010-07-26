<Div id="proposal">

<p class="submitted">
Proposal for a Miniconf submitted by
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
<p>${ h.line_break(c.proposal.abstract) | n}</p>
</blockquote>
</div>

<div class="abstract">
<p><em>Target Audience:</em>
${ c.proposal.audience.name }</p>
</div>

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
${ h.link_to('(stalk on Google)', url='http://google.com/search?q=%s+%s' % (person.firstname + " " + person.lastname, person.email_address)) }
${ h.link_to('(linux specific stalk)', url='http://google.com/linux?q=%s+%s' % (person.firstname + " " + person.lastname, person.email_address)) }
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
${ len(a.content)/1024/1024 }MB
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
