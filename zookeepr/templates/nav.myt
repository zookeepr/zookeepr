<div id="navcontainer">
    <ul id="navlist">
        <li><a href="/" class="now">Home</a></li>
        <li><a href="/about" class="">About</a></li>
        <li><a href="/sponsors" class="">Sponsors</a></li>
        <li><a href="/media" class="">Media</a></li>
        <li><a href="/mini-confs" class="">Mini-confs</a></li>
        <li><a href="/contact" class="">Contact</a></li>
% if c.signed_in_person=='':
        <li> <%h.link_to('login / register', url=h.url(controller='account', action='signin', id=None)) %></li>
% else:
        <li> <%h.link_to('logout', url=h.url(controller='account', action='signout', id=None)) %></li>
% #endif
    </ul>
</div>
