# app-wide menu
<div id="menubar">

<div id="logo">
# a dirty hack
<img src="/seven-head.png" nwidth="32" height="32">
</div>

<div id="menu">
i'm at templates/menu.myt

<br />

<% h.link_to('home', url=h.url('home')) %>

<% h.link_to('cfp', url=h.url(controller='cfp')) %>

<% h.link_to('submissions', url=h.url(controller='/submission', action='index')) %>

<% h.link_to('people', url=h.url(controller='/person', action='index')) %>

<% h.link_to('sponsors') %>

</div>

<& account.myc:signin &>

<div class="clear">&nbsp;</div>

</div>

<div class="clear">&nbsp;</div>
