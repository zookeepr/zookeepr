<div id="menu">

<ul>
<li><% h.link_to('about', url=h.url(controller='about', action='index')) %></li>
#<li><% h.link_to('programme', url=h.url(controller='programme', action='index')) %></li>
<li><% h.link_to('sponsors', url=h.url(controller='about', action='sponsors')) %></li>
<li class="last"><% h.link_to('contact', url=h.url(controller='about', action='contact')) %></li>
</ul>

</div>
