
% if h.lca_info['cfp_status'] == 'not_open':
      The CFP is not open.
% elif h.lca_info['cfp_status'] == 'open':
<p id="cfpbutton" class="right"><% h.link_to('<img src="/cfp-go.png" alt="Call for Papers" /><br />Submit a paper for linux.conf.au 2008!', url='/cfp/submit') %></p>
% else:
      The CFP is closed.
% # endif


