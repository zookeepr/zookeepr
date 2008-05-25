<h1><% c.proposal.title | h %></h1>

<p>
<% paras(c.proposal.abstract) %>
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

<% paras(person.bio) %>
% #endfor

<%method title>
Programme // Talk Details - <& PARENT:title &>
</%method>

<%init>
import re
def paras(s):
  if not s:
    return ''
  if '<p>' in s:
    return s
  return re.sub(r'\n', '<br>', s)
</%init>
