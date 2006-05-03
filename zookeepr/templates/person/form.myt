<p><label for="person.handle">Handle:</label><br />
<% h.text_field('person.handle', c.person.handle) %></p>

<p><label for="person.email_address">Email Address:</label><br />
<% h.text_field('person.email_address', c.person.email_address) %></p>

<p><label for="person.password">Password:</label><br />
<% h.password_field('person.password') %></p>

<p><label for="person.firstname">First name:</label><br />
<% h.text_field('person.firstname', c.person.firstname) %></p>

<p><label for="person.lastname">Last name:</label><br />
<% h.text_field('person.lastname', c.person.lastname) %></p>

<p><label for="person.phone">Phone number:</label><br />
<% h.text_field('person.phone', c.person.phone) %></p>

<p><label for="person.fax">Fax number:</label><br />
<% h.text_field('person.fax', c.person.fax) %></p>
