<%python scope="init">
from zookeepr.lib.account import profile_url
</%python>

<ul id="usermenu" class="linkmenu">

% if r.environ.has_key('REMOTE_USER') and profile_url(r.environ['REMOTE_USER']) is not None:
<li><% h.link_to('my profile', url=profile_url(r.environ['REMOTE_USER'])) %></li>
<li><% h.link_to('sign out', url=h.url(controller='/account', action='signout')) %></li>
% else:
<li><% h.link_to('sign in', url=h.url(controller='/account', action='signin')) %></li>
% #endif
</ul>
