<%inherit file="/base.mako" />

<h2>Zookeepr configuration values</h2>

% if len(c.all_config) > 0:
<table>
	<tr>
		<th>Category</th>
		<th>Key</th>
		<th>Value</th>
	</tr>
% for line in c.all_config:
	<tr class="${ h.cycle('even', 'odd')}">
		<td>${ line.category }</td>
		<td>${ line.key }</td>
		<td>${ line.value }</td>
	</tr>
% endfor
</table>
% endif
