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
                                            <h1>
                              Welcome to ${ c.config.get('event_name') }!</h1>

% if c.db_content is not None:
  <p class="lead">
  ${ c.db_content.body | n }
  </p>
% else:
  <p>
    To put content here create a page with a URL of <u>/home</u> in the
    <a href="${ h.url_for(controller='db_content', action='new') }">page database</a>.
  </p>
% endif

<%def name="short_title()"><%
  return "Homepage"
%></%def>
