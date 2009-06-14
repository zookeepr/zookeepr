<%def name="toolbox_extra()">
  <li><em>Reviewer</em></li>
  <li><a href="/review/help">How to review</a></li>
  <li>${ h.link_to('Review proposals', url=h.url_for(controller='proposal', action='review_index')) }</li>
  <li>${ h.link_to('Your reviews', url=h.url_for(controller='review', action='index')) }</li>
  <li>${ h.link_to('Summary of proposals', url=h.url_for(controller='proposal', action='summary')) }</li>
  <li>${ h.link_to('Reviewer summary', url=h.url_for(controller='review', action='summary')) }</li>
  <li>${ h.link_to('Change proposal statuses', url=h.url_for(controller='proposal', action='approve')) }</li>
  <li>List of proposals by:</li>
  <ul class="indent">
    <li><a href="/admin/proposals_by_strong_rank">number of certain score / number of reviewers</a></li>
    <li><a href="/admin/proposals_by_max_rank">max score, min score then average</a></li>
    <li><a href="/admin/proposals_by_stream">stream and score</a></li>
  </ul>
</%def>
