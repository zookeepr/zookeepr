<h2>Approve/disapprove talks</h2>

<div class="contents"><h3>Review Pages</h3>
<ul>
<& reviewer_sidebar.myt &>
</ul>
</div>

<% h.form(h.url()) %>
<table>
  <tr>
    <th>#</th>
    <th>Title</th>
    <th>Proposal Type</th>
    <th>Submitter(s)</th>
    <th>Current Status</th>
    <th>Change Status</th>
  </tr>
%   for s in c.proposals:
  <tr class="<% h.cycle('even', 'odd') %>">
    <td><% h.link_to("%d" % s.id, url=h.url(action='view', id=s.id)) %></td>
    <td><% h.link_to("%s" % (h.util.html_escape(s.title)), url=h.url(action='view', id=s.id)) %></td>
    <td><% s.type.name %></td>
    <td>
%     for p in s.people:
      <% h.link_to( "%s %s" % (p.firstname, p.lastname) or p.email_address or p.id, url=h.url(controller='person', action='view', id=p.id)) %><br>
%     #endfor
    </td>
    <td>
%     if s.id in c.highlight:
        <b><% s.status.name %></b>
%     else:
        <% s.status.name %>
%     #endif
    </td>
    <td>
      <select name="talk.<% s.id %>">
              <option value="-" SELECTED> - </option>
%     for status in c.statuses:
%         if status != s.status:
              <option value="<% status.name %>"><% status.name %></option>
%         #endif
%     #endfor
      </select>

    </td>
  </tr>
% #endfor
</table>
<p class="submit"><% h.submitbutton('Submit!') %></p>
<% h.end_form() %>

<%python>
</%python>

<%method title>
Approve proposals - <& PARENT:title &>
</%method>
