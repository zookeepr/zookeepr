<%inherit file="/base.mako" />

<div style="clear: both;"></div>
% if c.day == 'all':
    <h2>Schedule</h2>
    <h2>Monday</h2>
    <%include file="monday.mako" />
    <h2>Tuesday</h2>
    <%include file="tuesday.mako" />
    <h2>Wednesday</h2>
    <%include file="wednesday.mako" />
    <h2>Thursday</h2>
    <%include file="thursday.mako" />
    <h2>Friday</h2>
    <%include file="friday.mako" />
% elif c.day == 'monday':
    <h2>Miniconf Schedule for Monday</h2>
    <%include file="monday.mako" />
% elif c.day == 'tuesday':
    <h2>Miniconf Schedule for Tuesday</h2>
    <%include file="tuesday.mako" />
% elif c.day == 'wednesday':
    <h2>Schedule for Wednesday</h2>
    <%include file="wednesday.mako" />
% elif c.day == 'thursday':
    <h2>Schedule for Thursday</h2>
    <%include file="thursday.mako" />
% elif c.day == 'friday':
    <h2>Schedule for Friday</h2>
    <%include file="friday.mako" />
% endif

<p class="note"><i>Schedule is subject to change without notice.</i></p>

<%def name="title()">
Schedule - ${ parent.title() }
</%def>
