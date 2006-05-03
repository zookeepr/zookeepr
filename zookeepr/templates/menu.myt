# app-wide menu
<div id="menu">

i'm at templates/menu.myt

<br />

<% h.link_to('CFP', url=h.url(controller='cfp')) %>

<% h.link_to('Submissions', url=h.url(controller='/submission', action='index')) %>

<% h.link_to('People', url=h.url(controller='/person', action='index')) %>

</div>
