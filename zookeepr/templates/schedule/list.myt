<ul class = 'schedule_menu'>
    <li class = 'week_link'><a href = "">Entire Week</a></li>
    <li class = 'monday_link'><a href = "">Monday</a></li>
    <li class = 'tuesday_link'><a href = "">Tuesday</a></li>
    <li class = 'wednesday_link'><a href = "">Wednesday</a></li>
    <li class = 'thursday_link'><a href = "">Thursday</a></li>
    <li class = 'friday_link'><a href = "">Friday</a></li>
    <li class = 'saturday_link'><a href = "">Saturday</a></li>
</ul>
<div style="clear: both;"></div>
% if c.day.lower() == 'all':
    <h2>Schedule</h2>
    <& sunday.myt &>
    <& monday.myt &>
    <& tuesday.myt &>
    <& wednesday.myt &>
    <& thursday.myt &>
    <& friday.myt &>
    <& saturday.myt &>
% elif c.day.lower() == 'monday':
    <h2>Schedule for Monday</h2>
    <& monday.myt &>
% elif c.day.lower() == 'tuesday':
    <h2>Schedule for Tuesday</h2>
    <& tuesday.myt &>
% elif c.day.lower() == 'wednesday':
    <h2>Schedule for Wednesday</h2>
    <& wednesday.myt &>
% elif c.day.lower() == 'thursday':
    <h2>Schedule for Thursday</h2>
    <& thursday.myt &>
% elif c.day.lower() == 'friday':
    <h2>Schedule for Friday</h2>
    <& friday.myt &>
% elif c.day.lower() == 'saturday':
    <& saturday.myt &>
% #endif


<%method title>
Schedule - <& PARENT:title &>
</%method>
