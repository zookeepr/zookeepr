<p class="label"><span class="mandatory">*</span><label for="person.firstname">Your first name:</label></p>
<p class="entries"><% h.textfield('person.firstname', size=40) %></p>

<p class="label"><span class="mandatory">*</span><label for="person.lastname">Your last name:</label></p>
<p class="entries"><% h.textfield('person.lastname', size=40) %></p>

<p class="label"><span class="mandatory">*</span><label for="person.email_address">Email address:</label></p>
<p class="entries"><% h.textfield('person.email_address', size=70) %></p>
<p class="note">You will be using this email address to login, please make sure you don't typo.</p>

<p class="label"><span class="mandatory">*</span><label for="person.password">Choose a password:</label></p>
<p class="entries"><% h.passwordfield("person.password", size=40) %></p>

<p class="label"><span class="mandatory">*</span><label for="person.password_confirm">Confirm your password:</label></p>
<p class="entries"><% h.passwordfield("person.password_confirm", size=40) %></p>

<p><label for="person.phone">Phone number</label></p>
<p class="entries"><% h.textfield('person.phone') %></p>

<p><label for="person.mobile">Mobile/Cell number</label></p>
<p class="entries"><% h.textfield('person.mobile') %></p>
