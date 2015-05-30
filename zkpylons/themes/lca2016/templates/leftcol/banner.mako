<div id="myCarousel" class="carousel slide" data-ride="carousel">
%if len(c.db_content_banner) > 0:
<!-- Indicators -->
      <ol class="carousel-indicators">
   <% count = 0 %>
%   for d in c.db_content_banner:
%      if count == 0:
        <li data-target="#myCarousel" data-slide-to="0" class="active"></li>
%      else:
        <li data-target="#myCarousel" data-slide-to="${ count }"></li>
%      endif
      <% count = count + 1 %>
%   endfor
      </ol>
      <div class="carousel-inner" role="listbox">

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
<ol class="carousel-indicators">
<li data-target="#myCarousel" data-slide-to="0" class="active"></li>
</ol>
      <div class="carousel-inner" role="listbox">
        <div class="item active">
          <div class="container">
            <div class="carousel-caption">
              <h1>Currently no news</h1>
                </div>
              </div>
            </div>
%endif
</div>
      <a class="left carousel-control" href="#myCarousel" role="button" data-slide="prev">
        <span class="glyphicon glyphicon-chevron-left" aria-hidden="true"></span>
        <span class="sr-only">Previous</span>
      </a>
      <a class="right carousel-control" href="#myCarousel" role="button" data-slide="next">
        <span class="glyphicon glyphicon-chevron-right" aria-hidden="true"></span>
        <span class="sr-only">Next</span>
      </a>
    </div>

