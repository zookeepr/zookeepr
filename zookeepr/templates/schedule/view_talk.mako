<%inherit file="/base.mako" />

<p><a href="/programme/schedule/${ c.day }">&lt;-- Back to schedule</a></p>

<h2>${ c.talk.title | h }</h2>

<div id="proposal">
<div class="abstract">
<blockquote>
<p>${ h.line_break(h.url_to_link(c.talk.abstract)) | n}</p>
</blockquote>
</div>

% for person in c.talk.people:
<h2>${ person.firstname | h} ${ person.lastname | h}</h2>
<div class="bio">
<blockquote><p>
%   if person.bio:
${ h.line_break(h.url_to_link(person.bio)) }
%   else:
[none provided]
%   endif
</p></blockquote>
</div>

% endfor

</div>

<%def name="title()">
${ h.truncate(c.talk.title) } - ${ caller.title() }
</%def>
