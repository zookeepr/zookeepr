<%inherit file="/base.mako" />

<%

admin = 'organiser' in [r.name for r in h.signed_in_person().roles]

if admin:
  vouchers = c.voucher_collection
else:
  vouchers = c.signed_in_person.vouchers

%>

    <h2>Voucher Codes</h2>

% if admin:
    <p>This table lists all the voucher codes.</p>
% else:
    <p>This table lists the voucher codes for your group.</p>
%   if not vouchers:
    <p>(Note: you do not appear to be a group leader, so the table is blank.)</p>
%   endif
% endif

    <table>
      <tr>
        <th>Code</th>
        <th>Products</th>
% if admin:
        <th>Leader</th>
% endif
        <th>Comment</th>
        <th>Used By</th>
      </tr>

% for voucher in vouchers:
      <tr class="<% h.cycle('even', 'odd')%>">
        <td><% voucher.code %></td>
        <td>
%   if voucher.products:
%       for vproduct in voucher.products:
         <% vproduct.percentage %>% discount off <% vproduct.qty %> x <% vproduct.product.description %><br>
%       endfor
%   endif
        </td>
%   if admin:
        <td>
%       if voucher.leader:
          ${ voucher.leader.firstname |h} ${ voucher.leader.lastname |h}
          &lt;${ voucher.leader.email_address |h}&gt;
%       else:
          (no leader)
%       endif
        </td>
%   endif
        <td><% voucher.comment |h%></td>
%   if voucher.registration:
        <td><% voucher.registration.person.firstname %> <% voucher.registration.person.lastname %>
%          if voucher.registration.person.company:
           <% "(" + voucher.registration.person.company + ")"%>
%          endif
           &lt;<% voucher.registration.person.email_address %>&gt;
        </td>
%   else:
        <td><strong>Hasn't been used</strong></td>
%   endif
      </tr>
% endfor

    </table>

% if admin:
    <br>
    <p>${ h.link_to('Add another', url=h.url_for(controller='voucher',
    action='new')) }</p>
% endif

