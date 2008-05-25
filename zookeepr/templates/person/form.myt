<p class="label"><span class="mandatory">*</span><label for="person.firstname">Your first name:</label></p>
<p class="entries" valign="top"><% h.text_field('person.firstname', size=40) %></p>

<p class="label"><span class="mandatory">*</span><label for="person.lastname">Your last name:</label></p>
<p class="entries"><% h.text_field('person.lastname', size=40) %></p>

<p class="label"><span class="mandatory">*</span><label for="person.email_address">Email address:</label></p>
<p class="entries"><% h.text_field('person.email_address', size=70) %></p>
<p class="note">You will be using this email address to login, please make sure you don't typo.</p>

<p class="label"><span class="mandatory">*</span><label for="person.password">Choose a password:</label></p>
<p class="entries"><% h.password_field("person.password", size=40) %></p>

<p class="label"><span class="mandatory">*</span><label for="person.password_confirm">Confirm your password:</label></p>
<p class="entries"><% h.password_field("person.password_confirm", size=40) %></p>

<p><label for="person.phone">Phone number</label></p>
<p class="entries"><% h.text_field('person.phone') %></p>

% if c.mobile_is_mandatory:
<p class="label"><span class="mandatory">*</span>
% #endif
<p><label for="person.mobile">Mobile/Cell number</label></p>
<p class="entries"><% h.text_field('person.mobile') %></p>
