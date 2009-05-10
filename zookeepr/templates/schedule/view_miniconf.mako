<%inherit file="/base.mako" />

<p><a href="/programme/schedule/${ c.day }">&lt;-- Back to schedule</a>
<h2>${ c.talk.title | h }</h2>

<div id="proposal">
% if c.talk.url != None and c.talk.url != '':
<p><b>miniconf website: </b> <a href="${ c.talk.url }">${ c.talk.url }</a></p>
% endif

<div class="abstract">
<blockquote>
<p>${ h.line_break(h.url_to_link(h.remove_teaser_break(c.talk.abstract))) | n}</p>
</blockquote>
</div>
</div>

<%def name="title()">
${ h.truncate(c.talk.title) } - ${ caller.title() }
</%def>

