<li><a href="/review/help">How to review</a></li>
<li><% h.link_to('Review proposals', url=h.url(controller='proposal', action='review_index')) %></li>
<li><% h.link_to('Your reviews', url=h.url(controller='review', action='index')) %></li>
<li><% h.link_to('Summary of proposals', url=h.url(controller='proposal', action='summary')) %></li>
<li><% h.link_to('Reviewer summary', url=h.url(controller='review', action='summary')) %></li>
<li><% h.link_to('Change proposal statuses', url=h.url(controller='proposal', action='approve')) %></li>
