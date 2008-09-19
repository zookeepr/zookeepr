    <h2>New ceiling</h2>

    <% h.form(h.url(action='new')) %>
<& form.myt &>
      <p><% h.submitbutton("New") %>
      <% h.link_to('Back', url=h.url(action='index')) %></p>
    <% h.end_form() %>
