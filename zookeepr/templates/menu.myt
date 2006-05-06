<div id="menubar">

<div id="menu">
i'm at templates/menu.myt

<br />

<ul>
<li><% h.link_to('login') %></li></li>
<li><% h.link_to("what's on?") %></li>
<li><% h.link_to('programme') %></li>
<li><% h.link_to('dates') %></li>
<li><% h.link_to('press') %></li>
<li><% h.link_to('sydney') %></li>
<li><% h.link_to('contact') %></li>
<li><% h.link_to('sponsors') %></li>
<li><% h.link_to('home', url=h.url('home')) %></li>
</ul>
#<% h.link_to('cfp', url=h.url(controller='cfp')) %>

#<% h.link_to('submissions', url=h.url(controller='/submission', action='index')) %>

#<% h.link_to('people', url=h.url(controller='/person', action='index')) %>

</div>

#<& account.myc:signin &>

#<div class="clear">&nbsp;</div>

</div>

<div class="clear">&nbsp;</div>
