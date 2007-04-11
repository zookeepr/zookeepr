

% if c.cfp_status == 'not_open':
%     wiki_doc = '/wiki/cfp/not_open'
% elif c.cfp_status == 'open':
%     wiki_doc = '/wiki/cfp/open'
<p id="cfpbutton" class="right"><% h.link_to('<img src="/cfp-go.png" alt="Call for Papers" /><br />Submit a paper for linux.conf.au 2008!', url=h.url_for('submit_cfp')) %></p>
% else:
%     wiki_doc = '/wiki/cfp/closed'
% # endif


<% h.wiki_fragment(wiki_doc) %>

