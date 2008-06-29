<?xml version="1.0"?>
<rss version="2.0">
  <channel>
    <title>linux.conf.au News</title>
    <link>http://<% h.host_name() %></link>
    <description>Australia's annual Linux conference.</description>
    <language>en-us</language>
% for d in c.db_content_collection:
    <item>
      <title><% d.title %></title>
      <link>http://<% h.host_name() %>/media/news/<% d.id %></link>
      <description><% d.body |h %></description>
      <pubDate><% d.creation_timestamp.strftime("%a, %d %b %Y %H:%M:%S +1100") %></pubDate>
      <guid>http://linux.conf.au/media/news/<% d.id %></guid>
    </item>
% #endfor
  </channel>
</rss>
