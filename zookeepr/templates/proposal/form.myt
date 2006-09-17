<p>
<span class="mandatory">*</span>
<label for="proposal.title">Title:</label><br />
<% h.text_field('proposal.title', size=80) %></p>

<p>
<span class="mandatory">*</span>
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


<p>
<label for="proposal.url">Project URL:</label>
<br />
<% h.text_field('proposal.url', size=80) %>
</p>

<p>
<label for="attachment">Attach a paper:</label>
<% h.file_field('attachment', size=50) %>
</p>

<p>
<span class="mandatory">*</span>
<label for="proposal.abstract">Abstract:</label>
<br />
<% h.text_area('proposal.abstract', size="80x10") %></p>

<p>
<span class="mandatory">*</span>
<label for="proposal.experience">Experience:</label>
<br />
<% h.text_area('proposal.experience', size="80x5") %></p>

<p>
<span class="mandatory">*</span>
- Mandatory field
</p>
