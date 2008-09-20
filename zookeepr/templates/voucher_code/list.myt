    <h2>Voucher Codes</h2>

% if admin:
    <p>This table lists all the voucher codes.</p>
%   actionlink = h.link_to('Add another', url=h.url(controller='voucher_code', action='new'))
% else:
    <p>This table lists the voucher codes for your group.</p>
%   actionlink = ''
%   if not voucher_codes:
    <p>(Note: you do not appear to be a group leader, so the table is blank.)</p>
%   #endif
% #endif

    <table>
      <tr>
        <th>Code</th>
        <th>Product</th>
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
        <td><% d.product.description %></td>
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
%     if d.registration:
        <td><% d.registration.person.firstname %> <% d.registration.person.lastname %>
%          if d.registration.person.company:
           <% "(" + d.registration.person.company + ")"%>
%          # endif
           &lt;<% d.registration.person.email_address %>&gt;
        </td>
%     else:
        <td><strong>Hasn't been used</strong></td>
%     #endif
      </tr>
% #endfor

    </table>

    <br>
    <p><% actionlink %></p>

<%init>

admin = 'organiser' in [r.name for r in c.signed_in_person.roles]

if admin:
  voucher_codes = c.voucher_code_collection
else:
  voucher_codes = c.signed_in_person.voucher_codes

</%init>
