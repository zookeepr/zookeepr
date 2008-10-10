    <h2>Edit Volunteer</h2>
% if c.signed_in_person != c.volunteer.person:
    <p class="error-message">You're looking at (and editing) <% c.volunteer.person.firstname |h%> <% c.volunteer.person.lastname |h%>'s info, not your own!</p>
% #endif

% if errors:
      <p class="error-message">There
%   if len(errors)==1:
      is one problem
%   else:
      are <% `len(errors)` |h %> problems
%   #endif
      with your volunteer form, highlighted in red below. Please correct and re-submit.</p>
% #endif

<&| @zookeepr.lib.form:fill, defaults=defaults, errors=errors &>
    <% h.form(h.url(id=c.volunteer.id)) %>
<& form.myt &>
      <p><% h.submitbutton('Update') %></p>
    <% h.end_form() %>

</&>

<%args>
defaults
errors
</%args>

<%init>
if not defaults and c.volunteer:
    defaults = {}
    defaults['volunteer.other'] = c.volunteer.other
    if c.volunteer.areas:
        for area in c.volunteer.areas:
            defaults['volunteer.areas.' + area] = 1
</%init>
