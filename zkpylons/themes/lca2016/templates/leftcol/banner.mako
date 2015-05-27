%if len(c.db_content_banner) > 0:
   <% count = 0 %>
%   for d in c.db_content_banner:
%      if count == 0:
        <div class="item active">
%      else:
        <div class="item">
%      endif
	      ${ d.body |n }
	    </div>
	    <% count = count + 1  %>
%   endfor
%else:
        <div class="item active">
          <div class="container">
            <div class="carousel-caption">
              <h1>Currently no news</h1>
	        </div>
	      </div>
	    </div>
%endif
