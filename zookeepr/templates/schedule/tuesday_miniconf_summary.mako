<% day = 'tuesday' %>
<% miniconfs = [8, 32, 9, 108, 132, 116, 121, 26] %>
<% contents = '' %>
% for mid in miniconfs:
<%   miniconf = c.get_talk(mid) %>
<%   contents += '<li><a href="#' + day + '_' + h.computer_title(miniconf.title) + '">' + miniconf.title + '</li>' %>
% endfor

<div class="contents">
<h3>Tuesday's Miniconfs</h3>
<ul>
${ contents }
</ul>
</div>

% for mid in miniconfs:
<%include file="miniconf_link.mako", day=day, miniconf_id=mid />
% endfor
