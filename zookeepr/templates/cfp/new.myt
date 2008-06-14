<&| @zookeepr.lib.form:fill, defaults=defaults, errors=errors &>
<h1>Propose a talk or tutorial</h1>

<p>If you already have an account (from a previous proposal or otherwise) please <a href="<% h.url_for("/person/signin") %>">sign in</a> first, then return to this page.</p>

% if len(errors)>0:
<p class="error-message">Not submitted, sorry &mdash; there was a problem.
<br />Please see below for more details, edit and resubmit.</p>
%   for k in errors:
%     if errors[k] in ('Please enter a value', 'Missing value'):
%       errors[k]='This information is required.'
%     #endif
%   #endif
% #endif

<% h.form(h.url(), multipart=True) %>
<& form.myt &>

  <p class="submit"><% h.submitbutton('Submit!') %></p>
<% h.end_form() %>
</&>

<%method title>
Call for Papers - <& PARENT:title &>
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
        'person.experience': '',
        'person.bio': '',
        'proposal.type': 1,
        'proposal.assistance': 4,
    }
    if c.person:
        defaults['person.experience'] = c.person.experience
        defaults['person.bio'] = c.person.bio
</%init>
