%if len(c.db_content_press) > 0:
			<ul>
%   for d in c.db_content_press:
				<li><a href = '${ d.url |h }' class = 'external'>${ d.title }</a><div class="date">(${ h.domain_only(d.url) } - ${ d.creation_timestamp.strftime("%Y-%m-%d") })</div></li>
%   endfor
			</ul>
%else:
<p style="font-size: small;"><em>Currently no press...</em></p>
%endif
			<p class = 'more'><a href = '/media/in_the_press'>More items...</a></p>
