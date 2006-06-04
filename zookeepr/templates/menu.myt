<div id="menu">

<ul>
<li><% h.link_to('about', url=h.url(controller='about', action='view', id='index')) %></li>
#<li><% h.link_to('programme', url=h.url(controller='programme', action='index')) %></li>
<li><% h.link_to('sponsors', url=h.url(controller='about', action='view', id='sponsors')) %></li>
<li class="last"><% h.link_to('contact', url=h.url(controller='about', action='view', id='contact')) %></li>
</ul>

</div>
