<ul id="mainmenu" class="linkmenu">
<li><% h.link_to('about', url=h.url(controller='about', action='view', id='index')) %></li>
<li class="last"><% h.link_to('contact', url=h.url(controller='about', action='view', id='contact')) %></li>
</ul>
<br>
<ul id="mainmenu" class="sublinkmenu">
<li><% h.link_to('openday', url=h.url(controller='about', action='view', id='openday')) %></li>
<li><% h.link_to('partners', url=h.url(controller='about', action='view', id='partners')) %></li>
<li class="last"><% h.link_to('press', url=h.url(controller='about', action='view', id='press')) %></li>
</ul>
