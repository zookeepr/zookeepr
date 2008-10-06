% day = 'monday'
% miniconfs = [8, 157, 9, 132, 49, 116, 121, 26]
% contents = ''
% for mid in miniconfs:
%   miniconf = c.get_talk(mid)
%   contents += '<li><a href="#' + day + '_' + h.computer_title(miniconf.title) + '">' + miniconf.title + '</li>'
% #endfor

<div class="contents">
<h3>Monday's Miniconfs</h3>
<ul>
<% contents %>
</ul>
</div>

% for mid in miniconfs:
<& miniconf_link.myt, day=day, miniconf_id=mid &>
% #endfor
