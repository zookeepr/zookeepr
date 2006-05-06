<div id="menubar">

<div id="menu">
i'm at templates/menu.myt

<br />

<% h.link_to('login') %>
<% h.link_to("what's on?") %>
<% h.link_to('programme') %>
<% h.link_to('dates') %>
<% h.link_to('press') %>
<% h.link_to('sydney') %>
<% h.link_to('contact') %>
<% h.link_to('sponsors') %>
<% h.link_to('home', url=h.url('home')) %>

#<% h.link_to('cfp', url=h.url(controller='cfp')) %>

#<% h.link_to('submissions', url=h.url(controller='/submission', action='index')) %>

#<% h.link_to('people', url=h.url(controller='/person', action='index')) %>

</div>

#<& account.myc:signin &>

#<div class="clear">&nbsp;</div>

</div>

<div class="clear">&nbsp;</div>
