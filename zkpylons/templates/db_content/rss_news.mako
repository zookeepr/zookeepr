<?xml version="1.0"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>${ c.config.get("event_name") } News</title>
    <link>http://${ c.config.get('event_host') }</link>
    <description>${ c.config.get("event_byline") }</description>
    <language>en-us</language>
% for d in c.db_content_collection:
    <item>
      <title>${ d.title }</title>
      <link>http://${ c.config.get('event_host') }/media/news/${ d.id }</link>
      <description>${ d.body }</description>
      <pubDate>${ d.creation_timestamp.strftime("%a, %d %b %Y %H:%M:%S +1000") }</pubDate>
      <guid>http://${ c.config.get('event_host') }/media/news/${ d.id }</guid>
    </item>
% endfor
    <atom:link href="http://${ c.config.get('event_host') }/media/news/rss" rel="self" type="application/rss+xml" />
  </channel>
</rss>
