<%namespace name="toolbox" file="/leftcol/toolbox.mako"/>
<%inherit file="/base.mako" />
<%def name="toolbox_extra_admin()">
  ${ toolbox.make_link('Edit Person', url=h.url_for(controller='person', action='edit', id=c.person.id)) }
  ${ toolbox.make_link('Edit Person Roles', url=h.url_for(controller='person', action='roles', id=c.person.id)) }
</%def>

<h2>${ c.person.firstname |h }'s profile</h2>

<table>
    <tr>
        <td><b>First name:</b></p></td>
        <td>${ c.person.firstname }</td>
    </tr>
    <tr>
        <td><b>Last name:</b></p></td>
        <td>${ c.person.lastname }</td>
    </tr>
    <tr>
        <td><b>Email:</b></p></td>
        <td>
% if not c.person.activated:
          ${ c.person.email_address }
%   if h.auth.authorized(h.auth.has_organiser_role):
          (${ h.link_to('mark as verified', '/person/confirm/' + c.person.url_hash) })
%   else:
          (not verified)
%   endif
% else:
<a href="mailto:${ c.person.email_address }">${ c.person.email_address }</a>
% endif
        </td>
    </tr>
% if h.auth.authorized(h.auth.has_organiser_role):
    <tr>
        <td><b>Badge printed:</b></td>
        <td>
          ${ c.person.badge_printed }
%   if c.person.badge_printed:
          (${ h.link_to('reprint badge', '/person/' + str(c.person.id) + '/reprint') })
%   endif
        </td>
    </tr>
% endif

% if c.person.special_registration is not None:
%   for special_registration in c.person.special_registration:
    <tr>
      <td><b>${ special_registration.special_offer.id_name }:</b></p></td>
      <td>${ special_registration.member_number }</td>
    </tr>
%   endfor
% endif
% if h.auth.authorized(h.auth.has_organiser_role):
    <tr>
      <td valign="top"><b>Roles:</b></td>
      <td>
%   if len(c.person.roles) > 0:
<%  first = True %>
%     for role in c.person.roles:
%       if first:
<%      first = False %>
%       else:
<br />
%       endif
<%
        if role.pretty_name is None or role.pretty_name == '':
          role_name = role.name 
        else:
          role_name = role.pretty_name 
%>
        ${ h.link_to(role_name, url=h.url_for(controller='role', action='view',id=role.id)) }
%     endfor
%   else:
        None
%   endif
      </td>
    </tr>
% endif
% if c.person.phone:
    <tr>
        <td><b>Phone:</b></td>
        <td>${ c.person.phone }</td>
    </tr>
% endif
% if c.person.mobile:
    <tr>
        <td><b>Mobile:</b></td>
        <td>${ c.person.mobile }</td>
    </tr>
% endif
% if c.person.company:
    <tr>
        <td><b>Company:</b></td>
        <td>${ c.person.company }</td>
    </tr>
% endif
    <tr>
        <td valign="top"><b>Address:</b></td>
        <td><p>${ c.person.address1 }<br>
% if c.person.address2:
                ${ c.person.address2 }<br>
% endif
                ${ c.person.city }<br>
                ${ c.person.state } ${ c.person.postcode }<br>
                ${ c.person.country }</td>
    </tr>
    <!-- tr>
      <td colspan="2" align="center"><b>Social Networking</b></td>
    </tr -->
% for sn in c.person.social_networks:
    <!-- tr>
      <td><img style="padding-right: 5px" src="/images/${ sn.logo }">${ sn.name }</td>
<%
  import re
  p = re.compile('(USER)')
  url =  p.sub(c.person.social_networks[sn], sn.url)
%>

      <td><a href="${ url }">${ c.person.social_networks[sn] }</a></td>
##      <td><a href="${ c.person.social_networks[sn].account_url() }">${ c.person.social_networks[sn].account_name }</a></td>
    </tr -->
% endfor
</table>

% if h.lca_info['cfp_status'] in ('open', 'closed') or h.lca_info['cfmini_status'] in ('open', 'closed'):
<h2>Submitted Proposals</h2>

%   if len(c.person.proposals) > 0:
<table>
  <tr class="odd">
    <th>Title</th>
    <th>Proposal Type</th>
    <th>Abstract</th>
    <th>Status</th>
    <th>&nbsp;</th>
  </tr>
%     for s in c.person.proposals:
  <tr class="${ h.cycle('even', 'odd') }">
    <td>${ h.link_to("%s" % (s.title), url=h.url_for(controller='proposal', action='view', id=s.id)) }</td>
    <td>${ s.type.name }</td>
    <td>${ h.truncate(s.abstract) | n}</td>
    <td>${ s.proposer_status }</td>
    <td>
%       if c.proposal_editing == 'open' or h.auth.authorized(h.auth.has_late_submitter_role):
      ${ h.link_to("edit", url=h.url_for(controller='proposal', action='edit', id=s.id)) }
%       endif
%       if not (s.accepted or s.withdrawn or s.declined):
      ${ h.link_to("withdraw", url=h.url_for(controller='proposal', action='withdraw', id=s.id)) }
%       endif
    </td>
  </tr>
%     endfor
</table>
%   else:
    <p>None submitted.</p>
%   endif
% endif

% if h.lca_info['funding_status'] in ('open', 'closed'):
<h2>Submitted Funding Applications</h2>

%   if len(c.person.funding) > 0 and ('open', 'closed') in h.lca_info['funding_status']:
<table>
  <tr class="odd">
    <th>Proposal Type</th>
    <th>Status</th>
    <th>&nbsp;</th>
  </tr>
%     for s in c.person.funding:
  <tr class="${ h.cycle('even', 'odd') }">
    <td>${ s.type.name }</td>
    <td>
%       if s.status.name == 'Pending':
      <i>Undergoing review</i>
%       elif s.status.name == 'Accepted':
      Accepted</p>
%       elif s.status.name == 'Withdrawn':
      Withdrawn
%       else:
      Declined
%       endif
    </td>
    <td>
      ${ h.link_to("view", url=h.url_for(controller='funding', action='view', id=s.id)) }
%       if s.status.name == 'Pending' or s.status.name == 'Accepted':
%         if h.lca_info['funding_editing'] == 'open':
      ${ h.link_to("edit", url=h.url_for(controller='funding', action='edit', id=s.id)) }
%         endif
      ${ h.link_to("withdraw", url=h.url_for(controller='funding', action='withdraw', id=s.id)) }
    </td>
  </tr>
%       endif
%     endfor
</table>

%   else:
    <p>None submitted.</p>
%   endif
% endif

% if h.auth.authorized(h.auth.has_organiser_role):
<h2>Registration</h2>

%   if c.person.registration is None:
This person hasn't registered yet.
%   else:
<p>${ h.link_to('View Registration', h.url_for(controller="registration", action='view', id=c.person.registration.id)) }</p>

%     if len(c.person.registration.notes) > 0:
<table>
  <tr>
    <th>By</th>
    <th>Note</th>
    <th>&nbsp;</th>
  </tr>
%       for n in c.person.registration.notes:
  <tr class="${ h.cycle('even', 'odd') }">
    <td valign="top">${ n.by.fullname() } <i>${ n.last_modification_timestamp.strftime("%Y-%m-%d&nbsp; %H:%M") | n}</i></td>
    <td valign="top">${ h.line_break(n.note) }</td>
    <td valign="top">${ h.link_to("edit", h.url_for(controller='rego_note', action='edit', id=n.id)) }
    ${ h.link_to("view", h.url_for(controller='rego_note', action='view', id=n.id)) }</td>
  </tr>
%       endfor
</table>
%     else:
<p>No registration notes</p>
%     endif

<p>${ h.link_to("Add New Note", h.url_for(controller='rego_note', action='new', rego_id=c.person.registration.id)) }</p>
%   endif

<h2>Raised Invoices</h2>

%   if len(c.person.invoices) > 0:
<table>
  <tr>
    <th>Invoice</th>
    <th>Created</th>
    <th>Amount</th>
    <th>Status</th>
    <th>Manual</th>
    <th>Payment(s)</th>
  </tr>
%     for i in c.person.invoices:
  <tr class="${ h.cycle('even', 'odd') }">
    <td>${ h.link_to(str(i.id), h.url_for(controller="invoice", action='view', id=i.id)) }</td>
    <td>${ i.creation_timestamp }</td>
    <td align="right">${ "$%.2f" % (i.total/100.0) }</td>
    <td>${ i.status }
%       if i.status == 'Unpaid' or i.total == 0:
            <span style="font-size: smaller;">(${ h.link_to('Void', h.url_for(controller="invoice", action="void", id=i.id)) })</span>
%       endif
%       if i.status == 'Invalid':
            <span style="font-size: smaller;">(${ h.link_to('Unvoid', h.url_for(controller="invoice", action="unvoid", id=i.id)) })</span>
%       endif
        </td>
        <td>${ h.yesno(i.manual) |n }</td>
        <td>
%       if i.good_payments.count() > 0:
%         for p in i.good_payments:
%           if p.amount_paid != i.total:
          <b>mismatch!</b>
%           endif
          ${ "$%.2f" % (p.amount_paid / 100.0) }
          <small>${ p.gateway_ref |h}</small>
%         endfor
%       elif i.bad_payments.count() > 0:
        Bad payment(s)!
%       else:
          -
%       endif
        </td>
      </tr>
%     endfor
    </table>

%   else:
    <p>None raised.</p>
%   endif
<p>${ h.link_to('New manual invoice', url=h.url_for(controller='invoice', action='new', id=None, person_id=c.person.id)) }</p>

% endif



<hr>

% if h.auth.authorized(h.auth.Or(h.auth.is_same_zkpylons_user(c.person.id), h.auth.has_organiser_role)):
${ toolbox.make_link('Edit', url=h.url_for(action='edit',id=c.person.id)) }
% endif
% if h.auth.authorized(h.auth.has_organiser_role):
${ toolbox.make_link('Edit Person Roles', url=h.url_for(action='roles',id=c.person.id)) }
% endif

<%def name="title()">
Profile -
${ c.person.firstname |h } ${ c.person.lastname |h } -
 ${ parent.title() }
</%def>
