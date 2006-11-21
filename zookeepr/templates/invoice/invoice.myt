<%init>
total = 0
</%init>

Invoice <% invoice.id %>

Linux Australia
ABN: 37


Description           Cost
% for item in invoice.items:
<% item.description %>	<% item.cost %>
%	total += item.cost
% #endif
----------------------------------
total:             <% total %>

<%args>
invoice
</%args>
