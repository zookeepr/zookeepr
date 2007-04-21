<&| @zookeepr.lib.form:fill, defaults=defaults, errors=errors &>
<h1>Propose a Mini-conf</h1>

% if len(errors)>0:
<span class="error-message">Not submitted, sorry &mdash; there was a problem.</span>
<br>Please see below for more details, edit and resubmit.
%   for k in errors:
%     if errors[k]=='Please enter a value':
%       errors[k]='This information is required.'
%     #endif
%   #endif
% #endif

<% h.form(h.url(), multipart=True) %>
<& form_mini.myt &>

	<span class="submit"><% h.submit('Submit!') %></span>
<% h.end_form() %>
</&>

<%method title>
Call for Mini-confs - <& PARENT:title &>
</%method>

<%args>
defaults
errors
</%args>

<%init>
# Working around a bug in formencode, we need to set the defaults to the c.proposal
# values
if not defaults:
    defaults = {
        'person.experience': c.person.experience,
        'person.bio': c.person.bio
    }
</%init>
