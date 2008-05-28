<h2><% c.db_content.title %></h2>

<% menu %>

<% body %>

<%method title>
<% c.db_content.title %> - <& PARENT:title &>
</%method>

<%init>

import re
menu = ''
findh3 = re.compile('(<h3>(.+?)</h3>)', re.IGNORECASE|re.DOTALL|re.MULTILINE)
h3 = findh3.findall(c.db_content.body)
body = c.db_content.body
if h3 is not None:
    simple_title = ''
    body = findh3.sub(r'<a name="\g<2>"></a>\g<0>', body)
    menu = '<div class="contents"><h3>Contents</h3><ul>'
    for match in h3:
        menu += '<li><a href="#' + match[1] + '">' + match[1] + '</a></li>'
    menu += '</ul></div>'

</%init>
