% if r.environ.has_key('REMOTE_USER') and r.environ['REMOTE_USER'] == 'erik@meganerd.net':
<h1><% h.link_to('<img src="/sicktux.png" alt="linux.conf.au 2007" />', url=h.url('home')) %></h1>
% else:
<h1><% h.link_to('<img src="/lca2007.png" alt="linux.conf.au 2007" />', url=h.url('home')) %></h1>
%
