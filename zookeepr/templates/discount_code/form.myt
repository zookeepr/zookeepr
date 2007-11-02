<h2>Add a discount code</h2>

<div style="width: 600px; margin: auto;">

<fieldset>

<p>
<span class="mandatory">*</span>
<label for="discount_code.count">Count:</label>
<% h.text_field('discount_code.count', size=5) %>
<br />
<span class="fielddesc">How many discount codes to generate.</span>
</p>

<p>
<span class="mandatory">*</span>
<label for="discount_code.leader_id">Group leader:</label>
<% h.text_field('discount_code.leader_id', size=5) %>
<br />
<span class="fielddesc">ID of person who should be given the codes and
allowed to see who's using them, as per <a href="/profile">the profile
list</a>. If nobody, use your own ID: <% c.signed_in_person.id %></span>
</p>

<p>
<label for="discount_code.code">Code prefix:</label>
<% h.text_field('discount_code.code', size=40) %>
<br />
<span class="fielddesc">If you enter "foo", it might generate
"foo-ooH4epe7". If blank, it'll just generate "ooH4epe7". Theoretically it
might be a good idea to avoid 1, I, 0 and O, but I'm not sure how else one
would spell IBM or GOOGLE :-) </span>
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
