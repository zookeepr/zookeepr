<%inherit file="/base.mako" />

<h2>Delete Social Network</h2>

${ h.form(h.url_for()) }

<p> Are you sure you want to delete the (${ c.social_network.name }) social network?</p>

% if len(c.social_network.people) > 0:
<p> It is used by ${ len(c.social_network.people) } 
%   if len(c.social_network.people) == 1:
person.
%   else:
people.
%   endif
</p>
% endif

<p>${ h.submit('submit', 'Delete') }
 or ${ h.link_to('No, take me back.', url=h.url_for(action='index', id=None)) }</p>

${ h.end_form() }

<%def name="title()">
Social Network -
${ c.social_network.name } -
Confirm Delete -
 ${ parent.title() }
</%def>

