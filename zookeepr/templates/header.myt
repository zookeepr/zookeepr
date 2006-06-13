% if r.environ.has_key('REMOTE_USER') and r.environ['REMOTE_USER'] == 'erikd@mega-nerd.net':
%   logo = '/sicktux.png'
% else:
%   logo = '/lca2007.png'
%
<h1><% h.link_to('<img src="' + logo + '" alt="linux.conf.au 2007" />', url=h.url('home')) %></h1>
