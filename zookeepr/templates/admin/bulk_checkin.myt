<% h.form(h.url(), method='post') %>
<p class="entries">IDs: <% h.text_area('ids', size="10x10", tabindex=1) %></p>

<p class="entries">text: <% h.text_field('note', size=30, tabindex=2, value='Here! (bulk)') %></p>

<p class="entries">time: <% h.text_field('entered', size=20, tabindex=3, value=now) %></p>

<p class="submit"><% h.submit("Submit!") %></p>

<% h.end_form() %>
<%init>
from datetime import datetime
now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
</%init>
