<%def name="bookmark_submit(url, title='')">
<div class="bookmark_submit">
<%
 if len(title) == 0:
    title = c.config.get("event_byline")
 endif
 twit_title = title + ': ';
%>

  <a href="http://del.icio.us/post?url=${ url }"><img src="/img/sm_icons/delicious.png" width="32" height="32" alt="[D]" title="Submit to Del.icio.us"></a>
  <a href="http://digg.com/submit?phase=2&amp;url=${ url }"><img src="/img/sm_icons/digg.png" width="32" height="32" alt="[Digg]" title="Submit to Digg"></a>
  <a href="http://facebook.com/sharer.php?t=${ h.url_escape(title + ' ' + c.config.get("event_hashtag")) }&u=${ url }"><img src="/img/sm_icons/facebook.png" width="32" height="32" alt="[SU]" title="Set status on Facebook"></a>
  <a href="http://reddit.com/submit?url=${ url }"><img src="/img/sm_icons/reddit.png" width="32" height="32" alt="[R]" title="Submit to Reddit"></a>
  <a href="http://www.stumbleupon.com/submit?url=${ url }"><img src="/img/sm_icons/stumble.png" width="32" height="32" alt="[SU]" title="Submit to Stumble Upon"></a>
  <a href="http://twitter.com/home?status=${ h.url_escape(twit_title + url + ' ' + c.config.get("event_hashtag")) }"><img src="/img/sm_icons/twitter.png" width="32" height="32" alt="[SU]" title="Set status on Twitter"></a>
</div>
</%def>

