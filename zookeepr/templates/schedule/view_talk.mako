<%inherit file="/base.mako" />

<p><a href="/programme/schedule/${ c.day }">&lt;-- Back to schedule</a></p>

<h2>${ c.talk.title | h }</h2>

<table>
% if c.talk.scheduled:
  <tr class="${ h.cycle('even', 'odd')}">
    <td><strong>Time:</strong></td><td>${ c.talk.scheduled.strftime("%H:%M") } - ${ c.talk.finished.strftime("%H:%M") }</td>
  </tr>
  <tr class="${ h.cycle('even', 'odd')}">
    <td><strong>Day:</strong></td><td>${ c.talk.scheduled.strftime("%A %d %B %Y") }</td>
  </tr>
% endif

% if c.talk.theatre:
  <tr class="${ h.cycle('even', 'odd')}">
    <td><strong>Location:</strong></td><td>${ c.talk.theatre }
%   if c.talk.building:
  (${ c.talk.building })
%   endif
    </td>
  </tr>
% endif

% if c.talk.project or c.talk.url:
  <tr class="${ h.cycle('even', 'odd')}">
    <td><strong>Project:</td>
    <td>
%   if c.talk.url:
## FIXME: I reckon this should go into the helpers logic
%     if '://' in c.talk.url:
      <a href="${ c.talk.url | h }">
%     else:
      <a href="http://${ c.talk.url | h }">
%     endif
%   endif
%   if c.talk.project:
${ c.talk.project }
%   endif
%   if c.talk.url:
%     if not c.talk.project:
${ c.talk.url }
%     endif
</a>
%   endif
% endif
</td>

% if c.talk.type.name.startswith('Tutorial'):
  <tr class="${ h.cycle('even', 'odd')}">
    <td><strong>Wiki Page:</td>
    <td><a href="/wiki/Tutorials/${ c.talk.title }">${ c.talk.title }</a></td>
  </tr>
% endif

</table>


% for person in c.talk.people:
<div id="proposal">
<div class="abstract">
<blockquote>
<p>${ h.line_break(h.url_to_link(c.talk.abstract)) | n}</p>
</blockquote>
</div>

<h2>${ person.firstname | h} ${ person.lastname | h}</h2>
<div class="bio">
<blockquote><p>
%   if person.bio:
${ h.line_break(h.url_to_link(person.bio)) | n  }
%   else:
[none provided]
%   endif
</p></blockquote>
</div>

% endfor

</div>

<%def name="title()">
${ h.truncate(c.talk.title) } - ${ parent.title() }
</%def>
