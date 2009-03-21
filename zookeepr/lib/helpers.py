"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
# Import helpers as desired, or define your own, ie:
#from webhelpers.html.tags import checkbox, password

from webhelpers.html import escape, HTML, literal, url_escape
from webhelpers.html.tags import *
from webhelpers.html.secure_form import secure_form


# TODO Not 100% sure this is the right way to get url
from pylons import url


import os.path, random, array


from zookeepr.config.lca_info import lca_info, lca_rego, lca_menu, lca_submenus, file_paths

#from routes import url

# FIXME Commenting all this out till after we port to new pylons
#from routes import request_config
#from webhelpers import *
#import urllib
#from glob import glob
#import gzip, re
#
#def counter(*args, **kwargs):
#    """Return the next cardinal in a sequence.
#
#    Every time ``counter`` is called, the value returned will be the next
#    counting number in that sequence.  This is reset to ``start`` on every
#    request, but can also be reset by calling ``reset_counter()``.
#
#    You can optionally specify the number you want to start at by passing
#    in the ``start`` argument (defaults to 1).
#
#    You can also optionally specify the step size you want by passing in
#    the ``step`` argument (defaults to 1).
#
#    Sequences will increase monotonically by ``step`` each time it is
#    called, until the heat death of the universe or python explodes.
#
#    This can be used to count rows in a table::
#
#        # In Myghty
#        % for item in items:
#        <tr>
#            <td><% h.counter() %></td>
#        </tr>
#        % #endfor
#
#    You can used named counters to prevent clashes in nested loops.
#    You'll have to reset the inner cycle manually though.  See the
#    documentation for ``webhelpers.text.cycle()`` for a similar
#    example.
#    """
#    # optional name of this list
#    name = kwargs.get('name', 'default')
#    # optional starting value for this sequence
#    start = kwargs.get('start', 1)
#    # optional step size of this sequence
#    step = kwargs.get('step', 1)
#
#    counters = request_config().environ.setdefault('railshelpers.counters', {})
#
#    # ripped off of itertools.count
#    def do_counter(start, step):
#        while True:
#            yield start
#            start += step
#
#    counter = counters.setdefault(name, do_counter(start, step))
#
#    return counter.next()
#
#def reset_counter(name='default'):
#    """Resets a counter.
#
#    Resets the counter so that it starts from the ``start`` cardinal in
#    the sequence next time it is used.
#    """
#    del request_config().environ['railshelpers.counters'][name]
#
#def radio(name, value, label=None):
#    id_str = "%s.%s" % (name, value)
#    i = '<input type="radio" name="%s" id="%s" value="%s">' % (name, id_str, value)
#    if label is None:
#        lab = ''
#    else:
#        lab = '<label for="%s">%s</label>' % (id_str, label)
#    return i + lab
#
#def textarea(name, size):
#    temp = size.split("x")
#    return '<textarea name="%s" id="%s" cols="%s" rows="%s"></textarea>' % (name, name, temp[0], temp[1])
#
#def textfield(name, size=40, value=None, disabled=False):
#    enabled = ''
#    if disabled:
#        enabled = ' disabled="disabled"'
#    if value is None:
#        return '<input type="text" name="%s" id="%s" size="%s"%s>' % (name, name, size, enabled)
#    else:
#        return '<input type="text" name="%s" id="%s" size="%s" value="%s"%s>' % (name, name, size, value, enabled)
#
#def hiddenfield(name, value=None, size=40, disabled=False):
#    enabled = ''
#    if disabled:
#        enabled = ' disabled="disabled"'
#    if value is None:
#        return '<input type="hidden" name="%s" id="%s" size="%s"%s>' % (name, name, size, enabled)
#    else:
#        return '<input type="hidden" name="%s" id="%s" size="%s" value="%s"%s>' % (name, name, size, value, enabled)
#
#def passwordfield(name, size=40):
#    return '<input type="password" name="%s" id="%s" size="%s">' % (name, name, size)
#
#def submitbutton(value, name="Commit"):
#    return '<input  name="%s" type="submit" value="%s">' % (name, value)
#
#def webmaster_email(text=None):
#    """ E-mail link for the conference contact.
#
#    Renders a link to the committee; optionally takes a text, which will be
#    the text of the anchor (defaults to the e-mail address).
#    """
#    email = request_config().environ['paste.config']['app_conf']['webmaster_email']
#    if text==None:
#      text = '<tt>'+email+'</tt>'
#    return '<a href="mailto:'+email+'">'+text+'</a>'
#
#def contact_email(text=None):
#    """ E-mail link for the conference contact.
#
#    Renders a link to the committee; optionally takes a text, which will be
#    the text of the anchor (defaults to the e-mail address).
#    """
#    email = lca_info['contact_email']
#    if text == None:
#        text = '<tt>'+email+'</tt>'
#    return '<a href="mailto:'+email+'">'+text+'</a>'
#
#def host_name():
#    """ Name of the site (hostname)
#
#    Returns the fqdn for the website.
#    """
#    return request_config().environ['paste.config']['app_conf']['host_name']
#
#def event_name():
#    """ Name of the event
#
#    Returns the name of the event we're running (yay).
#    """
#    return lca_info['event_name']
#
#def get_temperature():
#    """ Fetch temperature from the BOM website.
#
#    This *REALLY* need to implement some sort of caching mechanism. Sadly I know no
#    python, so someone else is going to have to write it.
#    """
#    return urllib.urlopen('http://test.mel8ourne.org/dyn/temp.php').read()
#
#def array_random(a):
#    """Randomize the array
#    """
#    b = []
#    while len( a ) > 0:
#        j = random.randint(0, len( a ) - 1)
#        b.append( a.pop( j ) )
#    return b
#
#def random_pic(subdir):
#    """Mel8ourne random pic code.
#    """
#    fileprefix = '/srv/zookeepr/zookeepr/public/random-pix/'
#    htmlprefix = '/random-pix/'
#    try:
#        file = os.path.basename(random.choice(glob(fileprefix + subdir + '/*')))
#        return htmlprefix+subdir+'/'+file
#    except IndexError:
#        return "no images found"
#
#esc_re = re.compile(r'([<>&])')
#def esc(s):
#    """ HTML-escape the argument"""
#    def esc_m(m):
#      return {'>': '&gt;', '<': '&lt;', '&': '&amp;'}[m.group(1)]
#    if s is None:
#      return ''
#    try:
#      return esc_re.sub(esc_m, s)
#    except:
#      return esc_re.sub(esc_m, `s`)
#
#break_re = re.compile(r'(\n|\r\n)')
#def line_break(s):
#    """ Turn line breaks into <br>'s """
#    return break_re.sub('<br>', s)
#
#def yesno(bool):
#    """ Display a read-only checkbox for the value provided """
#    if bool:
#        return '&#9745;'
#    else:
#        return '&#9744;'
#
#def num(x):
#    """ Display a number or none if a number wasn't entered """
#    if x==None:
#        return 'none'
#    else:
#        return x
#
#def date(d):
#    """ Display a date in text format (currently limited to the month that is hardcoded) """
#    if d==1:
#        return "%dst of January" % d
#    elif d==2:
#        return "%dnd of January" % d
#    elif d==3:
#        return "%drd of January" % d
#    elif d<15:
#        return "%dth of January" % d
#    elif d==31:
#        return "%dst of January" % d
#    else:
#        return "%dth of January" % d
#
#def countries():
#    """ list of countries, as retrieved from the miscfiles package
#        (stripping of all diacritical marks)
#    """
#    res = []
#    import unicodedata as ud
#    for line in gzip.open('/usr/share/misc/countries.gz').readlines():
#        if line[0]=='#' or line=='\n':
#            continue
#        cc = line.split(':')[3].decode('utf8')
#        s = ''
#        for ch in cc:
#            s += ud.normalize('NFD', ch)[0]
#        res.append(s)
#    res.sort()
#    return res
#
#def debug():
#    if request_config().environ['paste.config']['global_conf']['debug'] == "true":
#        return True
#    else:
#        return False
#
#teaser_re = re.compile(r'(\<\!\-\-break\-\-\>)')
#def make_teaser(body):
#    if teaser_re.search(body):
#        parts = teaser_re.split(body)
#        return parts[0], True
#    else:
#        return body, False
#
#def remove_teaser_break(body):
#    if teaser_re.search(body):
#        return teaser_re.sub('', body)
#    else:
#        return body
#
#_news_id = -1
#def news_id():
#    global _news_id
#    if _news_id == -1:
#        from sqlalchemy.orm import create_session
#        from zookeepr.model import DBContentType
#        _news_id = create_session().query(DBContentType).filter_by(name='News').first().id
#    return _news_id
#
#def is_news(article_id):
#    if news_id() == article_id:
#        return True
#    return False
#
#computer_re = re.compile(r'([^A-Za-z0-9\_\-])')
#def computer_title(title):
#    """ Turn a string into a computer friendly tag """
#    title = title.replace(' ', '_')
#    title = computer_re.sub('', title)
#    title = title.lower()
#    return title
#
#def wiki_link(title):
#    """ Turn a string into a wiki friendly tag """
#    parts = title.split(' ')
#    title = ''.join([part.title() for part in parts])
#    title = computer_re.sub('', title)
#    return title
#
def featured_image(title, big = False):
    """
    Returns img src If an image exists in /public/featured/ with the same
    computer-friendly title as a news item it becomes featured down the left If
    big == True then find a directory
    """

    fileprefix = file_paths['news_fileprefix']
    htmlprefix = file_paths['news_htmlprefix']

    if big:
        # look for folder feature
        if os.path.isdir(fileprefix + "/" + computer_title(title)):
            return htmlprefix + "/" + computer_title(title) + "/"
        else:
            return False
    else:
        # look for image
        if os.path.isfile(fileprefix + "/" + computer_title(title) + ".png"):
            return htmlprefix + "/" + computer_title(title) + ".png"
        else:
            return False

    return False

#domain_re = re.compile('^(http:\/\/|ftp:\/\/)?(([a-z]+[a-z0-9]*[\.|\-]?[a-z]+[a-z0-9]*[a-z0-9]+){1,4}\.[a-z]{2,4})')
#def domain_only(url):
#    """ Truncates a url to the domain only. For use with "in the press" """
#    match = domain_re.match(url)
#    if match:
#        return match.group(2)
#    else:
#        return url
#
#def extension(name):
#    """ Return the extension of a file name"""
#    return name.split('.')[-1]
#
#def silly_description():
#    adverb = random.choice(lca_rego['silly_description']['adverbs'])
#    adjective = random.choice(lca_rego['silly_description']['adjectives'])
#    noun = random.choice(lca_rego['silly_description']['nouns'])
#    start = random.choice(lca_rego['silly_description']['starts'])
#    if start == 'a' and adverb[0] in ['a', 'e', 'i', 'o', 'u']:
#        start = 'an'
#    desc = '%s %s %s %s' % (start, adverb, adjective, noun)
#    descChecksum = silly_description_checksum(desc)
#    return desc, descChecksum
#
#def silly_description_checksum(desc):
#    import hashlib
#    return hashlib.sha1(desc).hexdigest()
#
#def ticket_percentage_text(percent, earlybird = False):
#    if percent == 100:
#        return 'All tickets gone.'
#    elif percent >= 97.5:
#        if earlybird:
#            return "Earlybird almost soldout."
#        else:
#            return "Almost all tickets gone."
#    else:
#        if earlybird:
#            return "%d%% earlybird sold." % percent 
#        else:
#            return "%d%% tickets sold." % percent
#
#link_re = re.compile(r'\[url\=((http:\/\/|ftp:\/\/)?(([a-z]+[a-z0-9]*[\.|\-]?[a-z]+[a-z0-9]*[a-z0-9]+){1,4}\.[a-z]{2,4})([^ \t\n]+))\](.*)\[\/url\]')
#def url_to_link(body):
#    """ Converts [url=http://example.com]site[/url] into <a href="http://www.example.com">site</a>> """
#    return link_re.sub(r'<a href="\1" title="\1">\6</a>', body)
