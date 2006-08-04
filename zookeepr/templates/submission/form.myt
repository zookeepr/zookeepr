<p><label for="submission.title">Title:</label><br />
<% h.text_field('submission.title', c.submission.title, size=80) %></p>

<p><label for="submission.submission_type">Type:</label><br />
<% h.text_field('submission.submission_type', c.submission.submission_type) %></p>

<p><label for="submission.abstract">Abstract:</label><br />
<% h.text_area('submission.abstract', c.submission.abstract, size="80x10") %></p>

<p><label for="submission.experience">Experience:</label><br />
<% h.text_area('submission.experience', c.submission.experience, size="80x5") %></p>

<p><label for="submission.url">URL:</label><br />
<% h.text_field('submission.url', c.submission.url, size=80) %></p>
