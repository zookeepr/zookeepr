<%inherit file="/base.mako" />

<h2>Approve/disapprove funding</h2>

${ h.form(h.url_for()) }
<table>
  <tr>
    <th>#</th>
    <th>Name</th>
    <th>Proposal Type</th>
    <th>Current Status</th>
    <th>Change Status</th>
  </tr>
%   for s in c.funding_requests:
  <tr class="${ h.cycle('even', 'odd') }">
    <td>${ h.link_to("%d" % s.id, url=h.url_for(action='view', id=s.id)) }</td>
    <td>
%     for p in s.people:
      ${ h.link_to( "%s %s" % (p.firstname, p.lastname) or p.email_address
      or p.id, url=h.url_for(controller='person', action='view', id=p.id)) }<br>
%     endfor
    </td>
    <td>${ s.type.name }</td>
    <td>
%     if s.id in c.highlight:
        <b>${ s.status.name }</b>
%     else:
        ${ s.status.name }
%     endif
    </td>
    <td>
      <select name="status-${ s.id }">
              <option value="" SELECTED> - </option>
%     for status in c.statuses:
%         if status != s.status:
              <option value="${ status.id }">${ status.name }</option>
%         endif
%     endfor
      </select>
      ${ h.hidden(name="request-%d"%s.id, value=s.id) }

    </td>
  </tr>
% endfor
</table>
<p class="submit">${ h.submit('submit', 'Submit!') }</p>
${ h.end_form() }

<%def name="title()" >
Approve funding requests - ${ parent.title() }
</%def>
