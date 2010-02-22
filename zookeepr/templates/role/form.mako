<p class="label"><span class="mandatory">*</span><label for="role.name">Name:</label></p>
<p class="entries">${ h.text('role.name') }</p>
<p class="note">The name of this role.  This should be lowercase, and contain no spaces.</p>

<p class="label"><label for="role.pretty_name">Pretty Name:</label></p>
<p class="entries">${ h.text('role.pretty_name') }</p>
<p class="note">The pretty name of this role.  This will be displayed in various places on the websites if it is set. If not set then this role will not be mentioned in public areas.</p>

<p class="label"><label for="role.comment">Comment:</label></p>
<p class="entries">${ h.text('role.comment') }</p>
<p class="note">What is the purpose of this role?</p>

<p class="label"><label for="role.display_order">Display Order:</label></p>
<p class="entries">${ h.text('role.display_order') }</p>
<p class="note">When displayed in a list, what position in the order should this entry have?</p>
