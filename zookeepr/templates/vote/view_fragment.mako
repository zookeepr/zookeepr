<p><b>Voting:</b> </p>
<p><b>By:</b> ${ h.link_to(c.vote.rego.person.firstname + ' ' +
c.vote.rego.person.lastname, h.url_for(controller='person',
action='view', id=c.vote.rego.person.id)) },

<p><b>Vote tokens used:</b> ${ c.vote.vote_value }</p>
<p><b>Comment:</b> ${ c.vote.comment }</p>

<p>${ h.link_to('Edit', h.url_for(controller='vote', action='edit',
id=c.vote.id)) } | ${ h.link_to('Back', h.url_for(controller='vote', action='index')) }</p>

<%def name="title()">
View note - ${ parent.title() }
</%def>
