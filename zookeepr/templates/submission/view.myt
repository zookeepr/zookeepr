<h2><% c.submission.title | h %></h2>

<div id="submission">

<p class="submitted">
<% c.submission.submission_type.name %> 
submitted by
<% c.submission.person.email_address %>
</p>

<p class="abstract">
<% c.submission.abstract | h %>
</p>

% if c.submission.url:
<p class="url">
<% h.link_to(c.submission.url, url=c.submission.url) %>
</p>
% #endif

<p class="experience">
<em>Speaking experience:</em>
% if c.submission.experience:
<br />
<% c.submission.experience | h %>
% else:
[none provided]
% #endif
</p>

<hr />

<p class="actions">
% if c.can_edit:
<% h.link_to('Edit', url=h.url(action='edit',id=c.submission.id)) %>
# |
% #end if
#<% h.link_to('Back', url=h.url(action='index')) %>
</p>

</div>
