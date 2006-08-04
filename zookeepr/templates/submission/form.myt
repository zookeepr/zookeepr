<p><label for="submission.title">Title:</label><br />
<% h.text_field('submission.title', c.submission.title, size=80) %></p>

<p><label for="submission.submission_type">Type:</label>
#<span class="fielddesc">What sort of submission is this?</span>
<br />

% for st in c.submission_types:
%	if c.submission.submission_type:
%		checked = st.id == c.submission.submission_type.id
%	else:
%		checked = False
%	#endif
<% h.radio_button('submission.submission_type', st.id, checked=checked) %>
<label for="submission.submission_type"><% st.name |h %></label><br />
% #endfor

</p>

<p><label for="submission.abstract">Abstract:</label><br />
<% h.text_area('submission.abstract', c.submission.abstract, size="80x10") %></p>

<p><label for="submission.experience">Experience:</label><br />
<% h.text_area('submission.experience', c.submission.experience, size="80x5") %></p>

<p><label for="submission.url">URL:</label><br />
<% h.text_field('submission.url', c.submission.url, size=80) %></p>
