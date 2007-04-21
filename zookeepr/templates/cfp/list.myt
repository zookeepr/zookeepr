
% if c.cfp_status == 'not_open':
      The CFP is not open.
% elif c.cfp_status == 'open':
<p id="cfpbutton" class="right"><% h.link_to('<img src="/cfp-go.png" alt="Call for Papers" /><br />Submit a paper for linux.conf.au 2008!', url=h.url_for('submit_cfp')) %></p>
% else:
      The CFP is closed.
% # endif


