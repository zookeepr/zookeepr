# app-wide menu
<div id="menubar">

<div id="logo">
# a dirty hack
<img src="/seven-head.png" nwidth="32" height="32">
</div>

<div id="menu">
i'm at templates/menu.myt

<br />

<% h.link_to('Home', url=h.url('home')) %>

<% h.link_to('CFP', url=h.url(controller='cfp')) %>

<% h.link_to('Submissions', url=h.url(controller='/submission', action='index')) %>

<% h.link_to('People', url=h.url(controller='/person', action='index')) %>

</div>

<& account.myc:signin &>

<div class="clear">&nbsp;</div>

</div>

<div class="clear">&nbsp;</div>
