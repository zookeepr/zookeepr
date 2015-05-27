<%inherit file="/base.mako" />

<h2>Approve/disapprove talks</h2>

${ h.form(h.url_for()) }
<table class="table sortable">
  <tr>
    <th>#</th>
    <th>Title</th>
    <th>Proposal Type</th>
    <th>Submitter(s)</th>
    <th>Current Status</th>
    <th>Change Status</th>
  </tr>
%   for s in c.proposals:
  <tr class="${ h.cycle('even', 'odd') }">
    <td>${ h.link_to("%d" % s.id, url=h.url_for(action='view', id=s.id)) }</td>
    <td>${ h.link_to("%s" % (h.util.html_escape(s.title)), url=h.url_for(action='view', id=s.id)) }</td>
    <td>${ s.type.name }</td>
    <td>
%     for p in s.people:
      ${ h.link_to( "%s %s" % (p.firstname, p.lastname) or p.email_address
      or p.id, url=h.url_for(controller='person', action='view', id=p.id)) }<br>
%     endfor
    </td>
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
      ${ h.hidden(name="talk-%d"%s.id, value=s.id) }

    </td>
  </tr>
% endfor
</table>
<p class="submit">${ h.submit('submit', 'Submit!') }</p>
${ h.end_form() }

<%def name="title()" >
Approve proposals - ${ parent.title() }
</%def>
