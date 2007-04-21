% try:
%   m.comp('content/'+url+'.myt')
% except:
%   try:
%     m.comp('content/'+url+'.html')
%   except:
<& error/404.myt &>
% #endtry

<%method title>
<% c.title %> - <& PARENT:title &>
</%method>

<%init>
# This file is used as a "last resort";
# it grabs a fragment out of the content/ subdirectory.

# For some reason, Myghty doesn't find components with unicode names...
url = c.url.encode('utf8')
</%init>
