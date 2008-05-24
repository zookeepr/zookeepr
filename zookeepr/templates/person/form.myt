<p><label for="person.email_address">Email Address</label>
<span class="fieldRequired">(Required)</span><br />
<% h.text_field('person.email_address') %></p>

<p><label for="person.password">Password</label>
<span class="fieldRequired">(Required)</span><br />
<% h.password_field('person.password') %></p>

<p><label for="person.password_confirm">Confirm password</label>
<span class="fieldRequired">(Required)</span><br />
<% h.password_field('person.password_confirm') %></p>

<p><label for="person.firstname">First name</label>
<br />
<% h.text_field('person.firstname') %></p>

<p><label for="person.lastname">Last name</label>
<br />
<% h.text_field('person.lastname') %></p>

# FIXME: this is a cheap switch based on the page name, not very robust
<p><label for="person.phone">Phone number</label>
% if m.request_path == h.url_for(controller='proposal', action='new'):
<span class="fieldRequired">(Required)</span><br />
% else:
<br />
%
<% h.text_field('person.phone') %></p>

<p><label for="person.mobile">Mobile number</label>
<br />
<% h.text_field('person.mobile') %></p>
