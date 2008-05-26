<p class="label"><span class="mandatory">*</span><label for="person.firstname">Your first name:</label></p>
<p class="entries"><% h.textfield('person.firstname', size=40) %></p>

<p class="label"><span class="mandatory">*</span><label for="person.lastname">Your last name:</label></p>
<p class="entries"><% h.textfield('person.lastname', size=40) %></p>

<p class="label"><span class="mandatory">*</span><label for="person.company">Company:</label></p>
<p class="entries"><% h.textfield('person.company', size=40) %></p>

<p class="label"><span class="mandatory">*</span><label for="person.email_address">Email address:</label></p>
<p class="entries"><% h.textfield('person.email_address', size=70) %></p>
<p class="note">You will be using this email address to login, please make sure you don't typo.</p>

<p class="label"><span class="mandatory">*</span><label for="person.password">Choose a password:</label></p>
<p class="entries"><% h.passwordfield("person.password", size=40) %></p>

<p class="label"><span class="mandatory">*</span><label for="person.password_confirm">Confirm your password:</label></p>
<p class="entries"><% h.passwordfield("person.password_confirm", size=40) %></p>

<p><label for="person.phone">Phone number</label></p>
<p class="entries"><% h.textfield('person.phone') %></p>

% if c.mobile_is_mandatory:
<p class="label"><span class="mandatory">*</span>
% #endif
<p><label for="person.mobile">Mobile/Cell number</label></p>
<p class="entries"><% h.textfield('person.mobile') %></p>


<p class="label">
<span class="mandatory">*</span>
<label for="person.address">Address:</label>
</p><p class="entries">
<% h.textfield('person.address1', size=40) %>
<br>
<% h.textfield('person.address2', size=40) %>
</p>
<p class="label">
<span class="mandatory">*</span>
<label for="person.city">City/Suburb:</label>
</p><p class="entries">
<% h.textfield('person.city', size=40) %>
</p><p class="label">
<label for="person.state">State/Province:</label>
</p><p class="entries">
<% h.textfield('person.state', size=40) %>
</p><p class="label">
<span class="mandatory">*</span>
<label for="person.country">Country:</label>
</p><p class="entries">
<select name="person.country">
% for country in h.countries():
<option value="<%country%>"><% country %></option>
% #endfor
</select>
</p><p class="label">
<span class="mandatory">*</span>
<label for="person.postcode">Postcode/ZIP:</label>
</p><p class="entries">
<% h.textfield('person.postcode', size=40) %>
</p>

