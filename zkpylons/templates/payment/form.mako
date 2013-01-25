<p>Generate a manual payment for ${ c.person.fullname }.</p>

<p class="label"><span class="mandatory">*</span>
<label for="payment.approved">Approved</label>
</p>
<p class="entries">
  <label>${ h.radio('payment.approved', 1) } Yes</label><br />
  <label>${ h.radio('payment.approved', 0) } No</label><br />
</p>

<p class="label"><span class="mandatory">*</span>
<label for="payment.success_code">Success Code</label>
</p>
<p class="entries">${ h.text('payment.success_code', size=40) }</p>

##<p class="label"><span class="mandatory">*</span>
##<label for="payment.response_text">Response Text</label>
##</p>
##<p class="entries">${ h.text('payment.response_text', size=40) }</p>

##<p class="label"><span class="mandatory">*</span>
##<label for="payment.payment">Payment ID</label>
##</p>
##<p class="entries">${ h.text('payment.payment', size=40) }</p>

<p class="label"><span class="mandatory">*</span>
<label for="payment.amount_paid">Amount Paid (in cents):</label>
</p>
<p class="entries">${ h.text('payment.amount_paid', size=40) }</p>

<p class="label"><span class="mandatory">*</span>
<label for="payment.currency_used">Currency:</label>
</p>
<p class="entries">${ h.text('payment.currency_used', size=40) }</p>

<p class="label">
<label for="payment.gateway_ref">Reference:</label>
</p>
<p class="entries">${ h.text('payment.gateway_ref', size=40) }</p>
<p class="note">Reference on bank statement, or other details</p>

##<p class="label">
##<label for="payment.card_name">Card Name:</label>
##</p>
##<p class="entries">${ h.text('payment.card_type', size=40) }</p>

##<p class="label">
##<label for="payment.card_number">Card Number:</label>
##</p>
##<p class="entries">${ h.text('payment.card_number', size=40) }</p>

##<p class="label">
##<label for="payment.card_expiry">Card Expiry:</label>
##</p>
##<p class="entries">${ h.text('payment.card_expiry', size=40) }</p>

<p class="label"><span class="mandatory">*</span>
<label for="payment.email_address">Email Address:</label>
</p>
<p class="entries">${ h.text('payment.email_address', size=40) }</p>

##<p class="label"><span class="mandatory">*</span>
##<label for="payment.client_ip_zookeepr">Client IP (Zookeepr):</label>
##</p>
##<p class="entries">${ h.text('payment.client_ip_zookeepr', size=40) }</p>

##<p class="label"><span class="mandatory">*</span>
##<label for="payment.client_ip_gatway">Client IP (Gateway):</label>
##</p>
##<p class="entries">${ h.text('payment.client_ip_gateway', size=40) }</p>
