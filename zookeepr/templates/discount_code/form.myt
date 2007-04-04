<h2>Add a discount code</h2>

<div style="width: 600px; margin: auto;">

<fieldset>

<p>
<span class="mandatory">*</span>
<label for="discount_code.code">Code:</label>
<% h.text_field('discount_code.code', size=40) %>
<br />
<span class="fielddesc">Suggest you use pwgen prefixed by something eg IBM-ahl3Oona</span>
</p>

<p>
<span class="mandatory">*</span>
<label for="discount_code.type">Rego Type</label>
<br />
# FIXME: dynamic content
% for t in ['Professional', 'Hobbyist', 'Concession']:
<input type="radio" name="discount_code.type" id="discount_code.type_<% t %>" value="<% t %>" />
<label for="discount_code.type_<% t %>"><% t %></label>
<br />
% #endfor
</p>

<p>
<span class="mandatory">*</span>
<label for="discount_code.percentage">Percentage Discount:</label>
<% h.text_field('discount_code.percentage', size=5) %>
<br />
<span class="fielddesc">Between 0-100</span>
</p>

<p>
<span class="mandatory">*</span>
<label for="discount_code.comment">Comment:</label>
<% h.text_field('discount_code.comment', size=60) %>
<br />
<span class="fielddesc">Why are they getting a discount?</span>
</p>
</fieldset>


</div>
