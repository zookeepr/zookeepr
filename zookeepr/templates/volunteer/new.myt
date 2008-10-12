    <h2>Volunteer</h2>

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
    <% h.form(h.url(action='new')) %>
<& form.myt &>
      <p><% h.submitbutton("New") %>
    <% h.end_form() %>
    </&>

<%args>
defaults
errors
</%args>
