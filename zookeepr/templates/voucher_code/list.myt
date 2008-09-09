<h2>Voucher Codes</h2>

% if admin:
This table lists all the voucher codes.
%   actionlink = h.link_to('(Add another)', url=h.url(controller='voucher_code', action='new'))
% else:
This table lists the voucher codes for your group.
%   actionlink = ''
%   if not voucher_codes:
(Note: you do not appear to be a group leader, so the table is blank.)
%   #endif
% #endif

<table>
    <tr>
        <th>Code</th>
        <th>Rego Type</th>
        <th>Disc.</th>
% if admin:
        <th>Leader</th>
% #endif
        <th>Comment</th>
        <th>Used By</th>
    </tr>

% for d in voucher_codes:
    <tr class="<% h.cycle('even', 'odd')%>">
        <td><% d.code %></td>
        <td><% d.type %></td>
        <td><% d.percentage %>%</td>
%    if admin:
        <td>
%      if d.leader:
          <% d.leader.firstname |h%> <% d.leader.lastname |h%>
          &lt;<% d.leader.email_address |h%>&gt;
%      else:
          (no leader)
%      #endif
        </td>
%    #endif
        <td><% d.comment |h%></td>
%     if d.registrations:
        <td><% d.registrations[0].person.firstname %> <% d.registrations[0].person.lastname %>
%          if d.registrations[0].company:
                <% "(" + d.registrations[0].company + ")"%>
%          # endif
           &lt;<% d.registrations[0].person.email_address %>&gt;
</td>
%     else:
        <td><strong>Hasn't been used</strong></td>
%     #endif
    </tr>
% #endfor

</table>

<br>
<% actionlink %>

<%init>

admin = 'organiser' in [r.name for r in c.signed_in_person.roles]

if admin:
  voucher_codes = c.voucher_code_collection
else:
  voucher_codes = c.signed_in_person.voucher_codes

</%init>
