<h1>My Proposals</h1>
<table>
  <tr>
    <th>Title</th>
    <th>Proposal Type</th>
    <th>Abstract</th>
    <th>Project URL</th>
    <th>Submitter(s)</th>
    <th>&nbsp;</th>
  </tr>
% for s in c.person.proposals:
  <tr class="<% h.cycle('even', 'odd') %>">
    <td><% h.link_to("%s" % (h.util.html_escape(s.title)), url=h.url(action='view', id=s.id)) %></td>
    <td><% s.type.name %></td>
    <td><% h.truncate(s.abstract) %></td>
    <td><% h.link_to(h.truncate(s.url), url=s.url) %></td>
    <td>
%   for p in s.people:
      <% h.link_to( "%s %s" % (p.firstname, p.lastname) or p.email_address or p.id, url=h.url(controller='person', action='view', id=p.id)) %>
%   #endfor
    </td>
    <td><% h.link_to("edit", url=h.url(controller='proposal', action='edit', id=s.id)) %></td>
  </tr>
% #endfor
</table>
<br>

<%python>
</%python>
 

<%method title>
Proposals - <& PARENT:title &>
</%method>
