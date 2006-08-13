#<% h.hidden_field('proposal.person_id', c.person.id) %>

<p><label for="proposal.title">Title:</label><br />
<% h.text_field('proposal.title', c.proposal.title, size=80) %></p>

<p>
<label for="proposal.proposal_type">Type:</label>
#<span class="fielddesc">What sort of proposal is this?</span>
<br />

% for st in c.proposal_types:
%	if c.proposal.type:
%		czeched = c.proposal.type == st
%	else:
%		czeched = False
%	#endif
<% h.radio_button('proposal.type', st.id, checked=czeched) %>
<label for="proposal.type"><% st.name |h %></label>
<br />
% #endfor

</p>

<p><label for="proposal.abstract">Abstract:</label><br />
<% h.text_area('proposal.abstract', c.proposal.abstract, size="80x10") %></p>

<p><label for="proposal.experience">Experience:</label><br />
<% h.text_area('proposal.experience', c.proposal.experience, size="80x5") %></p>

<p><label for="proposal.url">URL:</label><br />
<% h.text_field('proposal.url', c.proposal.url, size=80) %></p>
