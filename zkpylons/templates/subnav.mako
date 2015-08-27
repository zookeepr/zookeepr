<%
    # OVERRIDE THE MENUS BY OVERRIDING THIS FILE IN YOUR THEME
    # ========================================================

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

    # The current URL can be accessed as h.url()()
    url = h.url_for()
    # Hack for schedule url
    if url.startswith('/schedule'):
        url = '/programme' + url

    where = url.split('/')[1]


    def current(link):
        if url.startswith(link):
            return True
        else:
            return False

%>


% if submenus.has_key(where):
  <!-- Secondary navigation -->
  <div class="netv-nav">
          <div class="l"></div>
      <div class="r"></div>

        <ul class="netv-menu" style="background: #ccc !important">

%   for sub in submenus[where]:
<%
     link = sub.replace('/', '_').lower()
     link = '/'+where+'/'+link
     link = link.replace(' ', '_')
%>
%     if current(link):
            <li class="selected" style="background: #fff !important"><a href=""><span class="l"></span><span class="r"></span><span class="t">${ sub }</span></a></li>
%     else:
            <li><a href="${ link }"><span class="l"></span><span class="r"></span><span class="t">${ sub }</span></a></li>
%     endif
%   endfor
       </ul>
    </div>
% endif
