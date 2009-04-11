<%inherit file="/base.mako" />

<h2>My Proposals</h2>

%if len (c.person.proposals) > 0:
    <% declined = False %>

%  if c.paper_editing == 'closed':
<p>Proposal editing has been disabled while the review committee assess your proposals. Editing will be available later for updating details on your accepted presentations.</p>
%  endif
<p>Below is a list of proposals you have submitted. To view one click on the title; or to edit, click on the edit link.</p>
<table>
  <tr>
    <th>Title</th>
    <th>Proposal Type</th>
    <th>Abstract</th>
    <th>Project URL</th>
    <th>Submitter(s)</th>
    <th>Status</th>
    <th>&nbsp;</th>
  </tr>
%   for s in c.person.proposals:
  <tr class="${ h.cycle('even', 'odd') }">
    <td>${ h.link_to("%s" % (h.util.html_escape(s.title)), url=h.url_for(action='view', id=s.id)) }</td>
    <td>${ s.type.name }</td>
    <td>${ h.truncate(h.util.html_escape(s.abstract)) }</td>
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
    <td>
%     for p in s.people:
      ${ h.link_to( "%s %s" % (p.firstname, p.lastname) or p.email_address or p.id, url=h.url_for(controller='person', action='view', id=p.id)) }<br>
%     endfor
    </td>
    <td>
%     if s.accepted == None:
        <p><i>Undergoing review</i></p>
%     elif s.accepted:
        <p>Accepted</p>
%     else:
        <% declined = True %>
        <p>Declined<sup>[1]</sup></p>
%     endif    
    </td>
    <td>${ h.link_to("edit", url=h.url_for(controller='proposal', action='edit', id=s.id)) }</td>
  </tr>
% endfor
</table>

%   if declined:
<p>[1] Your proposal has been passed onto miniconf organisors for possible inclusion in their programmes. They <i>may</i> contact you.</p>
%   endif

%else:
    <p>You haven't submitted any proposals. To propose a miniconf, presentation or tutorial, please use the links above.</p>
%endif

<%def name="title()">
Proposals - ${ caller.title() }
</%def>
