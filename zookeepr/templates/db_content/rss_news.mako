<?xml version="1.0"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>${ h.lca_info["event_name"] } News</title>
    <link>http://${ h.host_name() }</link>
    <description>${ h.lca_info["event_byline"] }</description>
    <language>en-us</language>
% for d in c.db_content_collection:
    <item>
      <title>${ d.title }</title>
      <link>http://${ h.host_name() }/media/news/${ d.id }</link>
      <description>${ d.body |n }</description>
      <pubDate>${ d.creation_timestamp.strftime("%a, %d %b %Y %H:%M:%S +1000") }</pubDate>
      <guid>http://${ h.host_name() }/media/news/${ d.id }</guid>
    </item>
% endfor
    <atom:link href="http://${ h.host_name() }/media/news/rss" rel="self" type="application/rss+xml" />
  </channel>
</rss>
