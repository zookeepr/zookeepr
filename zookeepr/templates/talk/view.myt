<h2><% c.talk.title |h %></h2>

<p>A <% c.talk.type.name %> by
% for p in c.talk.people:
<% h.link_to(p.fullname, url=h.url(controller='profile', action='view', id=p.id)) %>
% #endfor
</p>

<div id="abstract">
<p>
<% c.talk.abstract |s %>
</p>
</div>

<%method title>
Abstract - <& PARENT:title &>
</%method>
