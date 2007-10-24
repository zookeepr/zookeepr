<h1><% c.proposal.title | h %></h1>

<p>
<% c.proposal.abstract.replace('\n', '<br/>') %>
</p>

<p>
Project:
% if c.proposal.url:
# FIXME: I reckon this should go into the helpers logic
%	if '://' in c.proposal.url:
<% h.link_to(c.proposal.project, url=c.proposal.url) %>
%	else:
<% h.link_to(c.proposal.project, url='http://' + c.proposal.url) %>
%	#endif
% else:
<% c.proposal.project %>
% #endif
</p>

% for person in c.proposal.people:
<h2><% person.firstname | h%> <% person.lastname | h%></h2>

%   if person.bio:
<% person.bio.replace('\n', '<br/>') %>
%   #endif
% #endfor

<%method title>
<% h.truncate(c.proposal.title) %> - <% c.proposal.type.name %> - <& PARENT:title &>
</%method>

