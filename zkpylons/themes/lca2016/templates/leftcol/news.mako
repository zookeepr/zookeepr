%if len(c.db_content_news) > 0:
   <% count = 0 %>
%   for d in c.db_content_news:
%      if count == 0:
        <div class="item active">
%      else:
        <div class="item">
%      endif
        <!--<img class="slide-{$ count }" src="data:image/gif;base64,R0lGODlhAQABAIAAAHd3dwAAACH5BAAAAAAALAAAAAABAAEAAAICRAEAOw==" alt="First slide">-->
          <div class="container">
            <div class="carousel-caption">
	          <h1>${ d.title } </h1>
	          <p>${ d.creation_timestamp.strftime("%Y-%m-%d") } </p>
	          <p>${ d.body } </p>
	          <p><a class="btn btn-lg btn-primary" href="/media/news" role="button">More News</a></p>
	        </div>
	      </div>
	    </div>
	    <% count = count + 1  %>
%   endfor
%else:
        <div class="item active">
          <!--<img class="slide-1" src="data:image/gif;base64,R0lGODlhAQABAIAAAHd3dwAAACH5BAAAAAAALAAAAAABAAEAAAICRAEAOw==" alt="First slide">-->
          <div class="container">
            <div class="carousel-caption">
              <h1>Currently no news</h1>
	        </div>
	      </div>
	    </div>
%endif
