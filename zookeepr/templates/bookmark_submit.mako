<%def name="bookmark_submit(url)">
<div class="bookmark_submit">

  <a href="http://del.icio.us/post?url=${ url }"><img src="/images/tag_delicious.gif" width="16" height="16" alt="[D]" title="Submit to Del.icio.us"></a>
  <a href="http://reddit.com/submit?url=${ url }"><img src="/images/tag_reddit.gif" width="20" height="17" alt="[R]" title="Submit to Reddit"></a>
  <a href="http://digg.com/submit?phase=2&amp;url=${ url }"><img src="/images/tag_digg.gif" width="16" height="14" alt="[Digg]" title="Submit to Digg"></a>
  <a href="http://www.stumbleupon.com/submit?url=${ url }"><img src="/images/tag_stumble.gif" width="16" height="16" alt="[SU]" title="Submit to Stumble Upon"></a>
</div>
</%def>

