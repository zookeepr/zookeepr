<%inherit file="/base.mako" />

<h2>Approve/disapprove funding</h2>

${ h.form(h.url_for()) }
<table class="table sortable">
  <tr>
    <th>#</th>
    <th>Name</th>
    <th>Proposal Type</th>
    <th>Current Status</th>
    <th>Change Status</th>
  </tr>
%   for s in c.requests:
  <tr class="${ h.cycle('even', 'odd') }">
    <td>${ h.link_to("%d" % s.id, url=h.url_for(action='view', id=s.id)) }</td>
    <td>${ h.link_to(s.person.fullname, url=h.url_for(controller='person', action='view', id=s.person.id)) }</td>
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
      ${ h.hidden(name="funding-%d"%s.id, value=s.id) }

    </td>
  </tr>
% endfor
</table>
<p class="submit">${ h.submit('submit', 'Submit!') }</p>
${ h.end_form() }

<%def name="title()" >
Approve funding requests - ${ parent.title() }
</%def>
