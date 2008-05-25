
<p class="label"><span class="mandatory">*</span><label for="registration.firstname">Your first name:</label></p>
<p class="entries" valign="top"><% h.text_field('registration.firstname', size=40) %></p>

<p class="label"><span class="mandatory">*</span><label for="registration.lastname">Your last name:</label></p>
<p class="entries"><% h.text_field('registration.lastname', size=40) %></p>

<p class="label"><span class="mandatory">*</span><label for="registration.email_address">Email address:</label></p>
<p class="entries"><% h.text_field('registration.email_address', size=70) %></p>
<p class="note">You will be using this email address to login, please make sure you don't typo.</p>

<p class="label"><span class="mandatory">*</span><label for="registration.password">Choose a password:</label></p>
<p class="entries"><% h.password_field("registration.password", size=40) %></p>

<p class="label"><span class="mandatory">*</span><label for="registration.password_confirm">Confirm your password:</label></p>
<p class="entries"><% h.password_field("registration.password_confirm", size=40) %></p>

# FIXME: this is a cheap switch based on the page name, not very robust
<p><label for="person.phone">Phone number</label>
<br />
<% h.text_field('person.phone') %></p>

<p><label for="person.mobile">Mobile/Cell number</label>
<br />
<% h.text_field('person.mobile') %></p>
