<%inherit file="/base.mako" />
<%def name="toolbox_extra_admin()">
  <li>${ h.link_to('Edit Person', url=h.url_for(controller='person', action='edit',id=c.person.id)) }</li>
  <li>${ h.link_to('Edit Person Roles', url=h.url_for(controller='person', action='roles',id=c.person.id)) }</li>
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
%if not c.person.activated:
${ c.person.email_address }
%  if h.auth.authorized(h.auth.has_organiser_role):
(${ h.link_to('mark as verified', '/person/confirm/' + c.person.url_hash) })
%  else:
(not verified)
%  endif
%else:
<a href="mailto:${ c.person.email_address }">${ c.person.email_address }</a>
%endif
        </td>
    </tr>
%if c.person.special_registration is not None:
% for special_registration in c.person.special_registration:
    <tr>
        <td><b>${ special_registration.special_offer.id_name }:</b></p></td>
        <td>${ special_registration.member_number }</td>
    </tr>
% endfor
%endif
% if h.auth.authorized(h.auth.has_organiser_role):
    <tr>
      <td valign="top"><b>Roles:</b></td>
      <td>
% if len(c.person.roles) > 0:
<%  first = True %>
%   for role in c.person.roles:
%     if first:
<%    first = False %>
%     else:
<br />
%     endif
<%
      if role.pretty_name is None or role.pretty_name == '':
        role_name = role.name 
      else:
        role_name = role.pretty_name 
%>
     ${ h.link_to(role_name, url=h.url_for(controller='role', action='view',id=role.id)) }
%    endfor
% else:
None
% endif
      </p></td>
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
    <tr>
      <td colspan="2" align="center"><b>Social Networking</b></td>
    </tr>
% for sn in c.person.social_networks:
    <tr>
      <td><img style="padding-right: 5px" src="/images/${ sn.logo }">${ sn.name }</td>
<%
  import re
  p = re.compile('(USER)')
  url =  p.sub(c.person.social_networks[sn], sn.url)
%>

      <td><a href="${ url }">${ c.person.social_networks[sn] }</a></td>
##      <td><a href="${ c.person.social_networks[sn].account_url() }">${ c.person.social_networks[sn].account_name }</a></td>
    </tr>
% endfor
</table>

<h2>Submitted Proposals</h2>

% if len(c.person.proposals) > 0:
<table>
  <tr class="odd">
    <th>Title</th>
    <th>Proposal Type</th>
    <th>Abstract</th>
    <th>Status</th>
    <th>&nbsp;</th>
  </tr>
%   for s in c.person.proposals:
  <tr class="${ h.cycle('even', 'odd') }">
    <td>${ h.link_to("%s" % (s.title), url=h.url_for(controller='proposal', action='view', id=s.id)) }</td>
    <td>${ s.type.name }</td>
    <td>${ h.truncate(h.util.html_escape(s.abstract)) | n}</td>
    <td>
%     if s.status.name == 'Pending':
        <p><i>Undergoing review</i></p>
%     elif s.accepted:
        <p>Accepted</p>
%     elif s.status.name == 'Withdrawn':
        <p>Withdrawn</p>
%     else:
        <p>Declined</p>
%     endif
    </td>
    <td>
%if s.status.name == 'Pending' or s.accepted:
%  if c.paper_editing == 'open' or h.auth.authorized(h.auth.has_late_submitter_role):
  ${ h.link_to("edit", url=h.url_for(controller='proposal', action='edit', id=s.id)) }
%  endif
${ h.link_to("withdraw", url=h.url_for(controller='proposal', action='withdraw', id=s.id)) }
    </td>
  </tr>
%endif
% endfor
</table>
%else:
    <p>None submitted.</p>
%endif

<h2>Submitted Funding Applications</h2>

% if len(c.person.funding) > 0:
<table>
  <tr class="odd">
    <th>Proposal Type</th>
    <th>Status</th>
    <th>&nbsp;</th>
  </tr>
%   for s in c.person.funding:
  <tr class="${ h.cycle('even', 'odd') }">
    <td>${ s.type.name }</td>
    <td>
%     if s.status.name == 'Pending':
        <i>Undergoing review</i>
%     elif s.status.name == 'Accepted':
        Accepted</p>
%     elif s.status.name == 'Withdrawn':
        Withdrawn
%     else:
        Declined
%     endif
    </td>
    <td>
      ${ h.link_to("view", url=h.url_for(controller='funding', action='view', id=s.id)) }
%if s.status.name == 'Pending' or s.status.name == 'Accepted':
%  if h.lca_info['funding_editing'] == 'open':
  ${ h.link_to("edit", url=h.url_for(controller='funding', action='edit', id=s.id)) }
%  endif
${ h.link_to("withdraw", url=h.url_for(controller='funding', action='withdraw', id=s.id)) }
    </td>
  </tr>
%endif
% endfor
</table>


%else:
    <p>None submitted.</p>
%endif



<hr>

% if h.auth.authorized(h.auth.Or(h.auth.is_same_zookeepr_user(c.person.id), h.auth.has_organiser_role)):
<ul><li>${ h.link_to('Edit', url=h.url_for(action='edit',id=c.person.id)) }</li></ul>
% endif
% if h.auth.authorized(h.auth.has_organiser_role):
<ul><li>${ h.link_to('Edit Person Roles', url=h.url_for(action='roles',id=c.person.id)) }</li></ul>
% endif

<%def name="title()">
Profile -
${ c.person.firstname |h } ${ c.person.lastname |h } -
 ${ parent.title() }
</%def>
