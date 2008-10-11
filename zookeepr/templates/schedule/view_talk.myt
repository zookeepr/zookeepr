<p><a href="/programme/schedule/<% c.day %>">&lt;-- Back to schedule</a>
<h2><% c.talk.title | h %></h2>

<div id="proposal">
<div class="abstract">
<blockquote>
<p><% h.line_break(h.url_to_link(h.esc(c.talk.abstract))) %></p>
</blockquote>
</div>

% for person in c.talk.people:
<h2><% person.firstname | h%> <% person.lastname | h%></h2>
<div class="bio">
<blockquote><p>
%   if person.bio:
<% h.line_break(h.url_to_link(h.esc(person.bio))) %>
%   else:
[none provided]
%   #endif
</p></blockquote>
</div>

% # endfor

</div>

<%method title>
<% h.truncate(c.talk.title) %> - <& PARENT:title &>
</%method>

