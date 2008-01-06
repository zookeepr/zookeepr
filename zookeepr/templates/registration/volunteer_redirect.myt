<h1>Volunteer sign-up</h1>

% if c.signed_in_person:

Please <a href="/registration/new">fill in the registration form</a>,
selecting the Volunteer ticket type.

% else:

You are not signed in to the website, so I can't tell what your status is.
<ul>

<li><i>If you have an existing sign-in</i> on the site, please <a
href="/account/signin">sign in</a>.</li>
%   session['sign_in_redirect'] = '/registration/volunteer'
%   session.save()

<li><i>Otherwise</i>, please <a href="/registration/new">fill in the
registration form</a>, selecting the Volunteer ticket type.</li>

</ul>

% #endif
