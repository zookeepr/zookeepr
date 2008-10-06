<h1>Volunteer sign-up</h1>

% if c.signed_in_person:

Please <% h.link_to('fill in the registration form', url=h.url(action='new')) %>, selecting the Volunteer ticket type.

% else:

You are not signed in to the website, so I can't tell what your status is.
<ul>

<li><i>If you have an existing sign-in</i> on the site, please <% h.link_to('sign in', url=h.url(controller='person', action='signin')) %>.</li>
%   session['sign_in_redirect'] = h.url_for(action='volunteer')
%   session.save()

<li><i>Otherwise</i>, please <% h.link_to('fill in the registration form', url=h.url(action='new')) %>, selecting the Volunteer ticket type.</li>

</ul>

% #endif
