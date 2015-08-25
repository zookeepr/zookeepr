<%
    submenus = {
        'about': ['linux.conf.au', 'lca2011 Ninjas', 'Venue', 'History', 'Linux/Open Source', 'Harassment'],
        'brisbane': ['About', 'Sightseeing'],
        'sponsors': ['Sponsors', 'Why Sponsor'],
        #'programme': ['About', 'Social Events', 'Open Day', 'Partners Programme'], # stage 0
        #'programme': ['About', 'Papers', 'Miniconfs', 'Presentations', 'Posters', 'Tutorials'], # stage 1
        #'programme': ['About', 'Keynotes', 'Miniconf Info', 'Papers Info', 'Social Events', 'Open Day', 'Partners Programme'], # stage 2
        #'programme': ['About', 'Keynotes', 'Miniconfs', 'Speakers Info', 'Social Events', 'Open Day', 'Partners Programme'], # stage 2a
        'programme': ['About', 'Keynotes', 'Miniconfs', 'Schedule', 'Social Events', 'Open Day', 'Partners Programme'], # stage 3
        #'programme': ['About', 'Keynotes', 'Miniconfs','Schedule','Social Events','Open Day', 'Partners Programme'], # stage 4?
        'register': ['Prices', 'Accommodation', 'Terms and Conditions'],
        #'register': ['Prices', 'Funding', 'Accommodation', 'Terms and Conditions'],
        #'register': ['Prices/Ticket types','Terms and Conditions','Accommodation','Partners programme'], # stage 4
        'media': ['News','In the press','Graphics']
    }

    url = h.url_for()

    # Hack for schedule url
    if url.startswith('/schedule'):
        url = '/programme' + url

    mm = [
        ('Home', '/', 'home'),
        ('About', '/about/linux.conf.au', 'about'),
        ('Brisbane', '/brisbane/about', 'brisbane'),
        ('Sponsors', '/sponsors/sponsors', 'sponsors'),
        ('Programme', '/programme/about', 'programme'),
        ('Register', '/register/prices', 'register'),
        #('Register', '/register/prices', 'register'), # -- Stage 4
        ('Media', '/media/news', 'media'),
        ('Contact', '/contact', 'contact'),
        #('Planet', 'http://planet.lca2011.linux.org.au', 'planet'),
        ('Wiki', '/wiki', 'wiki'),
    ]

    where = ''
    if url == '' or url == '/':
        where = 'home'

    map = [(u, c) for (t, u, c) in mm]

    for (u, w) in map:
        if url.startswith('/' + w):
            where = w

    def cls(part):
        if part == where:
            return 'class="selected"'
        else:
            return 'class=""'
%>
<div id="navbar" class="navbar-collapse collapse">
  <ul class="nav navbar-nav">
% for (t, u, c) in mm:
%   if c == 'selected':
          <li class="active">${ t |n }</li>
%   else:
%     if submenus.has_key(c):
          <li class="dropdown">
              <a href="#" class="dropdown-toggle" data-toggle="dropdown" role="button" aria-expanded="false">${ t }<span class="caret"></span></a>
              <ul class="dropdown-menu" role="menu">
%       for sub in submenus[c]:
          <%
          link = sub.replace('/', '_')
          link = '/'+t+'/'+link
          link = link.lower()
          link = link.replace(' ', '_')
          %>
                  <li><a href="${ link }">${ sub }</a></li>
%       endfor
              </ul>
          </li>
%     else:
          <li ${ cls(c) |n}><a href="${ u }">${ t }</a></li>
%     endif
%   endif
% endfor
      </ul>
</div>
