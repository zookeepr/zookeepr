<%init>
if c.signed_in_person and c.signed_in_person.email_address == 'erikd@mega-nerd.com':
	logo = '/sicktux.png'
else:
	logo = '/lca2007-header.png'
</%init>
<h1><% h.link_to(h.image_tag(logo, alt="linux.conf.au 2007"), url=h.url('home')) %></h1>
