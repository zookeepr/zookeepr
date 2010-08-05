## -- coding: utf-8 --
<%inherit file="/base.mako" />
<%
featured = []
count = 0
limit = 4
for d in c.db_content_news_all:
    if (h.featured_image(d.title) is not False) and (count < limit):
        featured.append(d)
        count += 1
%>


<!-- <img src = '/images/heightfix.png' class = 'heightfix' alt = ''> -->

                                            <h2 class="netv-postheader">
                              <img src="images/postheadericon.png" width="26" height="26" alt="postheadericon">
                              Welcome to linux.conf.au 2011!</h2>

${ c.db_content.body | n }

<%def name="short_title()"><%
  return "Homepage"
%></%def>
