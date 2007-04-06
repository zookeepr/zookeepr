<% h.wiki_fragment('OpenDayContent') %>


<h3>Register for Open Day</h3>

<p>
Please fill in the form as best you can.
</p>

<&| @zookeepr.lib.form:fill, defaults=defaults, errors=errors &>
<% h.form(h.url()) %>

<fieldset id="openday">
<h4>Open Day details</h4>

<p>
<span class="mandatory">*</span>
<label for="openday.fullname">Your full name:</label>
<% h.text_field('openday.fullname', size=40) %>
</p>

<p>
<span class="mandatory">*</span>
<label for="openday.email_address">Email address:</label>
<% h.text_field('openday.email_address', size=40) %>
<br />
<span class="fielddesc">
Your email address will only be used to correspond with you about the Open Day event. It will not be shown or used otherwise.
</span>
</p>

</p>

<p>
<span class="mandatory">*</span>
<label for="openday.opendaydrag">How many people are you bringing to Open Day:</label>
<% h.text_field('openday.opendaydrag', size=10) %>
</span>
</p>

<p>
# FIXME: dynamic :)
<label for="openday.heardfrom">Where did you hear about Open Day:</label>
<select name="openday.heardfrom">
<option value="-">-</option>
% for s in ['Education Today', 'Schooldays for Parents', 'DET', 'DEST']:
<option value="<%s%>"><% s %></option>
% #endfor
</SELECT>
Other: <% h.text_field('openday.heardfromtext') %>
</p>

<% h.submit("Submit!") %>
<span class="fielddesc">
If you encounter any problems signing up please email <% h.contact_email() %>
</span>


<% h.end_form() %>
</&>

<%args>
defaults
errors
</%args>

<%init>
</%init>

