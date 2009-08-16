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
        <td><a href="mailto:${ c.person.email_address }">${ c.person.email_address }</a></td>
    </tr>
% if h.auth.authorized(h.auth.has_organiser_role):
    <tr>
      <td valign="top"><b>Roles:</b></td>
      <td>
% if len(c.person.roles) > 0:
%   for role in c.person.roles:
%     if role.pretty_name is None or role.pretty_name == '':
${ role.name }
%     else:
${ role.pretty_name }
%     endif
%   endfor
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
