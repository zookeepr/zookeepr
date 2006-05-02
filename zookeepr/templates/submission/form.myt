<p><label for="submission.title">Title:</label><br />
<% h.text_field('submission.title', c.submission.title) %></p>

<p><label for="submission.submission_type">Type:</label><br />
<% h.text_field('submission.submission_type', c.submission.submission_type) %></p>

<p><label for="submission.abstract">Abstract:</label><br />
<% h.text_area('submission.abstract', c.submission.abstract) %></p>

<p><label for="submission.experience">Experience:</label><br />
<% h.text_area('submission.experience', c.submission.experience) %></p>

<p><label for="submission.url">URL:</label><br />
<% h.text_field('submission.url', c.submission.url) %></p>
