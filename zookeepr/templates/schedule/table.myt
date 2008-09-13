<h2>Schedule</h2>

% if c.day.lower() == 'all':
    <% sunday.myt %>
    <% monday.myt %>
    <% tuesday.myt %>
    <% wednesday.myt %>
    <% thursday.myt %>
    <% friday.myt %>
    <% saturday.myt %>
% else:
    <% monday.myt %>
% #endif


<%method title>
Programme - <& PARENT:title &>
</%method>
