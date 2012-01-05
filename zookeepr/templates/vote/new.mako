<%inherit file="/base.mako" />

<h2>Vote for your favourite event(s)</h2>
${ h.form(h.url_for(action='new')) }
<%include file="form.mako" />
<p>${ h.submit('submit', 'Save') }
% if c.rego_id:
${ h.link_to('Back', url=h.url_for(controller='registration', action='index')) }
% else:
${ h.link_to('Back', url=h.url_for(action='index')) }
% endif
</p>
${ h.end_form() }
% for t in c.time_slot:
   <h2>${t.start_time}</h2>
%   for s in c.schedule:
%     if s.time_slot_id == t.id:
%       for i in c.events:
%         if i.id == s.event_id and i.type_id == 3 and i.computed_title() not in ['Keynote 1','Keynote 2','Sysadmin Miniconf','Best Of #1','Best Of #2','Best Of #3','Best Of #4']:
          <p>event ${i.computed_title()} ${i.publish}</p>
%         endif
%       endfor
%     endif
%   endfor
% endfor
<%def name="title()">
New note - ${ parent.title() }
</%def>
