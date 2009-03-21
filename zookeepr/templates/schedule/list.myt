<ul class = 'schedule_menu'>
    <li class = 'week_link'><a href="/programme/schedule/all.html">Entire Week</a></li>
    <li class = 'monday_link'><a href="/programme/schedule/monday.html">Monday</a></li>
    <li class = 'tuesday_link'><a href="/programme/schedule/tuesday.html">Tuesday</a></li>
    <li class = 'wednesday_link'><a href="/programme/schedule/wednesday.html">Wednesday</a></li>
    <li class = 'thursday_link'><a href="/programme/schedule/thursday.html">Thursday</a></li>
    <li class = 'friday_link'><a href="/programme/schedule/friday.html">Friday</a></li>
    <li class = 'saturday_link'><a href="/programme/open_day">Saturday</a></li>
</ul>
<div style="clear: both;"></div>
% if c.day == 'all':
    <h2>Schedule</h2>
    <h2>Monday</h2>
    <& monday.myt &>
    <h2>Tuesday</h2>
    <& tuesday.myt &>
    <h2>Wednesday</h2>
    <& wednesday.myt &>
    <h2>Thursday</h2>
    <& thursday.myt &>
    <h2>Friday</h2>
    <& friday.myt &>
% elif c.day == 'monday':
    <h2>Miniconf Schedule for Monday</h2>
    <& monday.myt &>
% elif c.day == 'tuesday':
    <h2>Miniconf Schedule for Tuesday</h2>
    <& tuesday.myt &>
% elif c.day == 'wednesday':
    <h2>Schedule for Wednesday</h2>
    <& wednesday.myt &>
% elif c.day == 'thursday':
    <h2>Schedule for Thursday</h2>
    <& thursday.myt &>
% elif c.day == 'friday':
    <h2>Schedule for Friday</h2>
    <& friday.myt &>
% #endif

<p class="note"><i>Schedule is subject to change without notice.</i></p>


<%method title>
Schedule - <& PARENT:title &>
</%method>
