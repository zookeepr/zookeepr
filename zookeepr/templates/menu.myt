<%python scope="init">
from zookeepr.lib.account import profile_url
</%python>

<ul id="usermenu" class="linkmenu">

% if r.environ.has_key('REMOTE_USER'):
<li><% h.link_to('my profile', url=profile_url(r.environ['REMOTE_USER'])) %></li>
<li><% h.link_to('sign out', url=h.url(controller='/account', action='signout')) %></li>
% else:
<li><% h.link_to('sign in', url=h.url(controller='/account', action='signin')) %></li>
% #endif
</ul>

<ul id="mainmenu" class="linkmenu">
<li><% h.link_to('about', url=h.url(controller='about', action='view', id='index')) %></li>
#<li><% h.link_to('programme', url=h.url(controller='programme', action='index')) %></li>
<li><% h.link_to('sponsors', url=h.url(controller='about', action='view', id='sponsors')) %></li>
<li class="last"><% h.link_to('contact', url=h.url(controller='about', action='view', id='contact')) %></li>
</ul>
