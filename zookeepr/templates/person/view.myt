View person

(<a href="<% h.url_for(action='new') %>">new person</a>)
(<a href="<% h.url_for(action='index') %>">list persons</a>)

(<a href="<% h.url_for(action='edit') %>">edit this person</a>)
(<a href="<% h.url_for(action='delete') %>">delete this person</a>)

% for (label, key) in [('Handle', 'handle'), ('Firstname', 'firstname'), ('Lastname', 'lastname'), ('Email', 'email_address')]:
<p>
	<b><% label %>:</b>
	<% getattr(c.person, key) | h %>
</p>
% #endfor

<p>
	<b>Submissions:</b>
% for s in c.person.submissions:
<% h.link_to(s.title, url=h.url(controller='submission', action='view', id=s.id)) %>
% #end for

<hr />

% if c.can_edit:
<% h.link_to('Edit', url=h.url(action='edit', id=c.person.id)) %>
% #end if
<% h.link_to('back', url=h.url(action='index')) %>
