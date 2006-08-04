<h2><% c.submission.title | h %></h2>

<div id="submission">

<p class="submitted">
<% c.submission.submission_type.name %> 
submitted by
% if c.person and (c.person == c.submission.person):
you!
% else:
<% c.submission.person.email_address %>
% #endif
</p>

% if c.submission.url:
<p class="url">
<b>Project URL:</b><% h.link_to(c.submission.url) %>
</p>
% #endif

<p class="abstract">
<% c.submission.abstract | h %>
</p>

<p class="experience">
<em>Speaking experience:</em><br />
<% c.submission.experience | h %>
</p>

<hr />

<p class="actions">
% if c.can_edit:
<% h.link_to('Edit', url=h.url(action='edit',id=c.submission.id)) %> |
% #end if
<% h.link_to('Back', url=h.url(action='index')) %>
</p>

</div>
