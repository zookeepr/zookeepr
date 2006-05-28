<%args>
	title
</%args>

<div class="contentbox">
  <div class="contentboxR" id="contentboxT">
    <div class="contentboxC" id="contentboxTL"></div>
    <div class="contentboxC" id="contentboxTR"></div>
  </div>  

  <div id="contentboxMR">
    <h2><% title %></h2>
    <% m.content() %>
  </div>  

  <div class="contentboxR" id="contentboxB">
    <div class="contentboxC" id="contentboxBL"></div>
    <div class="contentboxC" id="contentboxBR"></div>
  </div>  
</div>
