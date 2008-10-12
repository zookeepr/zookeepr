<p><a href="/programme/schedule/<% c.day %>">&lt;-- Back to schedule</a>
<h2><% c.talk.title | h %></h2>

<div id="proposal">
% if c.talk.url != None and c.talk.url != '':
<p><b>miniconf website: </b> <a href="<% c.talk.url %>"><% c.talk.url %></a></p>
% #endif

<div class="abstract">
<blockquote>
<p><% h.line_break(h.url_to_link(h.esc(h.remove_teaser_break(c.talk.abstract)))) %></p>
</blockquote>
</div>
</div>

<%method title>
<% h.truncate(c.talk.title) %> - <& PARENT:title &>
</%method>

