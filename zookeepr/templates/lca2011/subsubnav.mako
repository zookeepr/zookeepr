<%
    # Provide the list of subsubmenus in here.
    submenus = c.subsubmenu
    url = h.url_for()
    # Hack for schedule url
    if url.startswith('/schedule'):
        url = '/programme' + url

    def cls(part):
        if part == url:
            return 'class="selected"'
        else:
            return 'class=""'

    def current(link):
        if url.startswith(link):
            return True
        else:
            return False

%>
% if submenus:
    <!-- Tertiary navigation -->
    <div class="netv-nav">
        <div class="l"></div>
        <div class="r"></div>
        <ul class="netv-menu" style="background: #99ff33 !important">

%   for (link, name) in submenus:
%     if current(link):
            <li class="selected" style="background: #7DB12F !important"><a href=""><span class="l"></span><span class="r"></span><span class="t">${ name }</span></a></li>
%     else:
            <li><a href="${ link }"><span class="l"></span><span class="r"></span><span class="t">${ name }</span></a></li>
%     endif
%   endfor
        </ul>
    </div>
% endif
