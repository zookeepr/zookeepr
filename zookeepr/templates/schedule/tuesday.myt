% miniconfs = [8, 32, 9, 108, 83, 116, 201, 26]
% contents = ''
% for mid in miniconfs:
%   miniconf = c.get_talk(mid)
%   contents += '<li><a href="#' + h.computer_title(miniconf.title) + '">' + miniconf.title + '</li>'
% #endfor

<div class="contents">
<h3>Monday's Miniconfs</h3>
<ul>
<% contents %>
</ul>
</div>

% for mid in miniconfs:
<& miniconf_link.myt, miniconf_id=mid &>
% #endfor
