% if c.person and c.person.email_address == 'erikd@mega-nerd.net':
%   logo = '/sicktux.png'
% else:
%   logo = '/lca2007-header.png'
% #endif
<h1><% h.link_to('<img src="' + logo + '" alt="linux.conf.au 2007" />', url=h.url('home')) %></h1>
