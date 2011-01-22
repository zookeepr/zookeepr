<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html lang="en-us">
<head>
  <title>Photocompetition Full Screen</title>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
  <script type="text/javascript" src="/jquery.min.js"></script>
  <script type="text/javascript" src="/js/galleria/galleria.js"></script>
  <script type="text/javascript" src="/js/galleria/themes/classic/galleria.classic.js"></script>
  <script type="text/javascript">
    function start_slidshow() {
      var gallery = jQuery('#gallery');
      var window_height = jQuery(window).height();
      gallery.attr("style", "height: " + window_height + "px");
      gallery.galleria({
        extend: function(options) {
          var slideShow = function() {
            this.play(3000);
          };
          var normalScreen = function() {
            history.back();
          };
          this.attachKeyboard({
            escape:     normalScreen,   // escape
            space:      slideShow,      // space
            backspace:  this.pause,     // return
            left:	this.prev,      // left
            right:      this.next,      // right
          });
          this.play(3000);
        },
      });
    }
  </script>
</head>

<body>
  <div id="gallery">
  %for photo in c.photos:
    <a href="/photocomp/photo/${photo.filename('1024x768')}"><img src="/photocomp/photo/${photo.filename('68x51')}" alt="${photo.filename('orig')}" title="${c.photo_title(photo)}"/></a>
  %endfor
  </div>
  <script type="text/javascript">
    start_slidshow();
  </script>
</body>
</html>
