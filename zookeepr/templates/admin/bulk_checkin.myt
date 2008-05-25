<% h.form(h.url(), method='post') %>
<p class="entries">IDs: <% h.textarea('ids', size="10x10", tabindex=1) %></p>

<p class="entries">text: <% h.textfield('note', size=30, tabindex=2, value='Here! (bulk)') %></p>

<p class="entries">time: <% h.textfield('entered', size=20, tabindex=3, value=now) %></p>

<p class="submit"><% h.submitbutton("Submit!") %></p>

<% h.end_form() %>
<%init>
from datetime import datetime
now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
</%init>
