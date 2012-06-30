<%inherit file="/base.mako" />

<h2>My Proposals</h2>

% if len(c.person.proposals) > 0:
<%
  footnotes = []

  fn_declined = "Your proposal has been passed onto miniconf organisers "
  fn_declined+= "for possible inclusion in their programmes. "
  fn_declined+= "They <i>may</i> contact you."

  fn_consent = "Please make sure that you are allowed to do this, if there "
  fn_consent+= "is any doubt (for instance, consider whether you're "
  fn_consent+= "revealing your employer's information or using other "
  fn_consent+= "people's copyrighted materials.)"

  fn_share = "Please consider allowing us to share both the video of "
  fn_share+= "your talk and your slides, so that the community can "
  fn_share+= "gain the maximum benefit from your talk!"
%>

%  if c.proposal_editing == 'closed':
<p>Proposal editing has been disabled while the review committee assess your proposals. Editing will be available later for updating details on your accepted presentations.</p>
%  endif
<p>Below is a list of proposals you have submitted. To view one click on the title; or to edit, click on the edit link.</p>
<table>
  <tr class="odd">
    <th>Title</th>
    <th>Proposal Type</th>
    <th>Abstract</th>
    <!--<th>Target Audience</th>-->
    <th>Project URL</th>
    <!--<th>Submitter(s)</th>-->
    <th>Consent</th>
    <th>Status</th>
    <th>&nbsp;</th>
  </tr>
%   for s in c.person.proposals:
  <tr class="${ h.cycle('even', 'odd') }">
    <td>${ h.link_to("%s" % (s.title), url=h.url_for(action='view', id=s.id)) }</td>
    <td>${ s.type.name }</td>
    <td>${ h.truncate(s.abstract) | n}</td>
    <!--<td>${ s.audience.name }</td>-->
%     if s.url:
## FIXME: I reckon this should go into the helpers logic
%       if '://' in s.url:
    <td>${ h.link_to(h.truncate(h.util.html_escape(s.url)), url=h.util.html_escape(s.url)) }</td>
%       else:
    <td>${ h.link_to(h.truncate(h.util.html_escape(s.url)), url=h.util.html_escape('http://'+s.url)) }</td>
%       endif
%     else:
    <td>&nbsp;</td>
%     endif
    <!--<td>
%     for p in s.people:
      ${ h.link_to( "%s %s" % (p.firstname, p.lastname) or p.email_address or p.id, url=h.url_for(controller='person', action='view', id=p.id)) }<br>
%     endfor
    </td>-->
    <td>
<%
     cons = []; fns = []
     if s.video_release:
         cons.append('video')
     if s.slides_release:
         cons.append('slides')
     if not cons:
         cons.append('no')
     if s.video_release or s.slides_release:
         fns.append(fn_mark(fn_consent))
     if not s.video_release or not s.slides_release:
         fns.append(fn_mark(fn_share))
     if fns:
        fns.sort()
        fns = '<sup>[' + ','.join(fns) + ']</sup>'
     else:
        fns = ''
%>
    ${ ' and '.join(cons) } release${ fns |n}
    </td>
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
%  if c.proposal_editing == 'open' or h.auth.authorized(h.auth.has_late_submitter_role):
  ${ h.link_to("edit", url=h.url_for(controller='proposal', action='edit', id=s.id)) }
%  endif
${ h.link_to("withdraw", url=h.url_for(controller='proposal', action='withdraw', id=s.id)) }
    </td>
  </tr>
%endif
% endfor
</table>

%   for fnmark, fn in enumerate(footnotes):
<p>[${ fnmark+1 }] ${ fn |n}</p>
%   endfor

%else:
    <p>You haven't submitted any proposals.</p>
%endif

<p><ul>
%  if c.cfp_status == 'open':
<li>${ h.link_to('New proposal', url=h.url_for(controller='proposal', action='new')) }</li>
%  endif
%  if c.cfmini_status == 'open':
<li>${ h.link_to('New miniconf proposal', url=h.url_for(controller='miniconf_proposal', action='new')) }</li>
%  endif
</ul></p>

<%def name="short_title()"><%
  return 'My Proposals'
%>
</%def>
<%def name="title()">
Proposals - ${ parent.title() }
</%def>

<%def name="fn_mark(text)">
<%
    if text not in footnotes:
        footnotes.append(text)
    return '%d' % (footnotes.index(text)+1)
%>
</%def>

