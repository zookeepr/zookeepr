<h2><% c.talk.title |h %></h2>

<p>A <% c.talk.type.name %> by
% for p in c.talk.people:
<% h.link_to(p.fullname, url=h.url(controller='profile', action='view', id=p.id)) %>
% #endfor
</p>

<div id="abstract">
#% content = h.wiki_here()
% content = h.wiki_fragment('/wiki/talk/%d' % c.talk.id)
% if 'This page does not exist yet.' in content:
<% c.talk.abstract |s %>
#<p><% h.link_to('Edit wiki', url=h.url('/talk/%d?action=edit' % c.talk.id)) %></p>
% else:
<% content %>
% #endif
</div>

<%method title>
Abstract - <& PARENT:title &>
</%method>
