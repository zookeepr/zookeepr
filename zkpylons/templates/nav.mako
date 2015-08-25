<%
    # OVERRIDE THE MENUS BY OVERRIDING THIS FILE IN YOUR THEME
    # ========================================================

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
<div class="netv-nav">
<div class="l"></div>
<div class="r"></div>
      <ul class="netv-menu">
% for (t, u, c) in mm:
%   if c == 'selected':
          <li>${ t |n }</li>
%   else:
          <li ${ cls(c) |n}><a href="${ u }"><span class="l"></span><span class="r"></span><span class="t">${ t }</span></a></li>
%   endif

% endfor
      </ul>
</div>
