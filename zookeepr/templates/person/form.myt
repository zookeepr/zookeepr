<p><label for="person.email_address">Email Address</label>
<span class="fieldRequired">(Required)</span><br />
<% h.text_field('person.email_address', c.person.email_address) %></p>

<p><label for="person.password">Password</label>
<span class="fieldRequired">(Required)</span><br />
<% h.password_field('person.password') %></p>

<p><label for="person.password_confirm">Confirm password</label>
<span class="fieldRequired">(Required)</span><br />
<% h.password_field('person.password_confirm') %></p>

<p><label for="person.handle">Username</label>
<br />
<% h.text_field('person.handle', c.person.handle) %></p>

<p><label for="person.firstname">First name</label>
<br />
<% h.text_field('person.firstname', c.person.firstname) %></p>

<p><label for="person.lastname">Last name</label>
<br />
<% h.text_field('person.lastname', c.person.lastname) %></p>

# FIXME: this is a cheap switch based on the page name, not very robust
<p><label for="person.phone">Phone number</label>
% if m.request_path == h.url_for(controller='submission', action='new'):
<span class="fieldRequired">(Required)</span><br />
% else:
<br />
%
<% h.text_field('person.phone', c.person.phone) %></p>

<p><label for="person.fax">Fax number</label>
<br />
<% h.text_field('person.fax', c.person.fax) %></p>
