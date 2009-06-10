<%
menu = ''
if c.db_content and not h.url_for().endswith('edit'):
  import re
  findh3 = re.compile('(<h3>(.+?)</h3>)', re.IGNORECASE|re.DOTALL|re.MULTILINE)
  h3 = findh3.findall(c.db_content.body)
  if h3.__len__() > 0:
    simple_title = ''
    for match in h3:
        simple_title = re.compile('([^a-zA-Z])').sub('', match[1])
        menu += '<li><a href="#' + simple_title + '">' + match[1] + '</a></li>'
%>

% if menu != '':
  <div class="yellowbox">
    <div class="boxheader">
      <h1>Contents</h1>
      <ul>
${ menu | n}
      </ul>
    </div>
  </div>
% endif

  <!-- Sponsors on left column -->
  <div class="whitebox">
    <div class="boxheader">
      <h1>Our Emperor Sponsors</h1>
      <ul>
        <li><a href="http://www.internetnz.org.nz"><img src="/sponsors/InternetNZ.png" alt="InternetNZ" title="Internet NZ works to keep the Internet open and uncaptureable, protecting and promoting the Internet for New Zealand." /></a></li>
      </ul>
    </div>
  </div>



