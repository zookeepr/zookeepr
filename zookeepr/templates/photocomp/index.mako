<%inherit file="/base.mako" />
<%namespace file="../bookmark_submit.mako" name="bookmark_submit" inheritable="True"/>

<h2>Photo Competition</h2>

<%
  import datetime
%>

<p>
  <a href="/photocomp/edit">Submit an entry</a>.
</p>

<h3>Entries</h4>

%if c.no_photos:

<p>
  There are no Photo Competition entries ready for viewing.
</p>

%elif not c.photos:

<p>
  There are no entries matching your filter.
</p>

%else:

<table style="border: none; padding: 0; margin: 0 0 10px 0;">
  <tr><td style="border: none; padding: 0; margin: 0;">
    <div id="gallery" style="height: 500px; width: 660px; z-index: 10000">
    %for photo in c.photos:
      <a href="/photocomp/photo/${photo.filename('1024x768')}"><img src="/photocomp/photo/${photo.filename('68x51')}" alt="${photo.filename('orig')}" title="${c.photo_title(photo)}"/></a>
    %endfor
    </div>
  </td></tr>
  <tr><td style="border: none; padding: 5px 0; margin: 0; text-align: center;">
    <a id="photo_caption" href="" target="_blank">&nbsp;</a>
  </td></tr>
</table>

<script type="text/javascript">
  start_slidshow();
</script>

%endif

${ h.form(h.url_for(), method='GET') }
<table style="border: none"><tr>
  <td style="border: none; padding: 0 5px; margin: 0; vertical-align: middle;">
    <label for="day">Day Filter</label>
    <select name="day">
      <option value="All"/>All</option>
    %for day in range(0, c.DAYS_OPEN):
      <option value="${ str(day) }">${(c.open_date + datetime.timedelta(day)).strftime('%A')}</option>
    %endfor
    </select>
  </td>
  <td style="border: none; padding: 0 5px; margin: 0; vertical-align: middle;">
    <label for="person">Person filter</label>
    <select name="person">
      <option value="All"/>All</option>
      %for person in c.all_person:
        <option value="${ str(person.id) }">${person.firstname} ${person.lastname}</option>
      %endfor
    </select>
  </td>
  <td style="border: none; padding: 0 5px; margin: 0; vertical-align: middle;">
    <input type=checkbox name="randomise"/><label for="randomise">Randomise?</label>
  </td>
  </td>
  <td style="border: none; padding: 0 5px 0 40px; margin: 0; vertical-align: middle; ">
    ${ h.submit("s", "Filter") }
  </td>
%if c.photos:
  <td style="border: none; padding: 0 0 0 5px; margin: 0; vertical-align: middle; ">
    ${ h.submit("s", "Full Screen") }
  </td>
%endif
</table>

${ h.end_form() }


<%def name="extra_head()">
<script type="text/javascript" src="/js/galleria/galleria.js"></script>
<script type="text/javascript" src="/js/galleria/themes/classic/galleria.classic.js"></script>
<script type="text/javascript">
  function start_slidshow() {
    var gallery = jQuery('#gallery');
    gallery.galleria({
      extend: function(options) {
        var slideShow = function() {
          this.play(3000);
        };
        this.attachKeyboard({
          space:      slideShow,      // space
          backspace:  this.pause,     // return
          left:	      this.prev,      // left
          right:      this.next,      // right
        });
        var image_displayed = function(e) {
          var a = jQuery("#photo_caption");
          var imageData = this.getData();
          a.attr("href", "/photocomp/photo/" +  imageData.description);
          a.html(imageData.title);
        };
        this.bind(Galleria.IMAGE, image_displayed);
        this.play(3000);
      },
    })
  }
</script>
</%def>
