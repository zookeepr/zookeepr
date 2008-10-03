<p><a href="/programme/schedule/<% c.day %>">&lt;-- Back to schedule</a>
<h2><% c.talk.title | h %></h2>

<div id="proposal">
<div class="abstract">
<blockquote>
<p><% h.line_break(h.esc(c.talk.abstract)) %></p>
</blockquote>
</div>
</div>

<%method title>
<% h.truncate(c.talk.title) %> - <& PARENT:title &>
</%method>

