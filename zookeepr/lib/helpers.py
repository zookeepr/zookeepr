"""
Helper functions

All names available in this module will be available under the Pylons h object.
"""
from routes import request_config
from webhelpers import *
import urllib
from glob import glob
import os.path, random, array
import gzip, re
from zookeepr.config.lca_info import lca_info, lca_rego, lca_menu, lca_submenus

def counter(*args, **kwargs):
    """Return the next cardinal in a sequence.

    Every time ``counter`` is called, the value returned will be the next
    counting number in that sequence.  This is reset to ``start`` on every
    request, but can also be reset by calling ``reset_counter()``.

    You can optionally specify the number you want to start at by passing
    in the ``start`` argument (defaults to 1).

    You can also optionally specify the step size you want by passing in
    the ``step`` argument (defaults to 1).

    Sequences will increase monotonically by ``step`` each time it is
    called, until the heat death of the universe or python explodes.

    This can be used to count rows in a table::

        # In Myghty
        % for item in items:
        <tr>
            <td><% h.counter() %></td>
        </tr>
        % #endfor

    You can used named counters to prevent clashes in nested loops.
    You'll have to reset the inner cycle manually though.  See the
    documentation for ``webhelpers.text.cycle()`` for a similar
    example.
    """
    # optional name of this list
    name = kwargs.get('name', 'default')
    # optional starting value for this sequence
    start = kwargs.get('start', 1)
    # optional step size of this sequence
    step = kwargs.get('step', 1)

    counters = request_config().environ.setdefault('railshelpers.counters', {})

    # ripped off of itertools.count
    def do_counter(start, step):
        while True:
            yield start
            start += step
            
    counter = counters.setdefault(name, do_counter(start, step))

    return counter.next()

def reset_counter(name='default'):
    """Resets a counter.

    Resets the counter so that it starts from the ``start`` cardinal in
    the sequence next time it is used.
    """
    del request_config().environ['railshelpers.counters'][name]

def radio(name, value, label=None):
    id_str = "%s.%s" % (name, value)
    i = '<input type="radio" name="%s" id="%s" value="%s">' % (name, id_str, value)
    if label is None:
        lab = ''
    else:
        lab = '<label for="%s">%s</label>' % (id_str, label)
    return i + lab

def textarea(name, size):
    temp = size.split("x")
    return '<textarea name="%s" id="%s" cols="%s" rows="%s"></textarea>' % (name, name, temp[0], temp[1])

def textfield(name, size=40, value=None, disabled=False):
    enabled = ''
    if disabled:
        enabled = ' disabled="disabled"'
    if value is None:
        return '<input type="text" name="%s" id="%s" size="%s"%s>' % (name, name, size, enabled)
    else:
        return '<input type="text" name="%s" id="%s" size="%s" value="%s"%s>' % (name, name, size, value, enabled)


def passwordfield(name, size=40):
    return '<input type="password" name="%s" id="%s" size="%s">' % (name, name, size)

def submitbutton(value, name="Commit"):
    return '<input  name="%s" type="submit" value="%s">' % (name, value)

def webmaster_email(text=None):
    """ E-mail link for the conference contact.

    Renders a link to the committee; optionally takes a text, which will be
    the text of the anchor (defaults to the e-mail address).
    """
    email = request_config().environ['paste.config']['app_conf']['webmaster_email']
    if text==None:
      text = '<tt>'+email+'</tt>'
    return '<a href="mailto:'+email+'">'+text+'</a>'

def contact_email(text=None):
    """ E-mail link for the conference contact.

    Renders a link to the committee; optionally takes a text, which will be
    the text of the anchor (defaults to the e-mail address).
    """
    email = lca_info['contact_email']
    if text == None:
        text = '<tt>'+email+'</tt>'
    return '<a href="mailto:'+email+'">'+text+'</a>'

def host_name():
    """ Name of the site (hostname)

    Returns the fqdn for the website.
    """
    return request_config().environ['paste.config']['app_conf']['host_name']

def event_name():
    """ Name of the event

    Returns the name of the event we're running (yay).
    """
    return lca_info['event_name']

def get_temperature():
    """ Fetch temperature from the BOM website.

    This *REALLY* need to implement some sort of caching mechanism. Sadly I know no
    python, so someone else is going to have to write it.
    """
    return urllib.urlopen('http://test.mel8ourne.org/dyn/temp.php').read()

def array_random(a):
    """Randomize the array
    """
    b = []
    while len( a ) > 0:
        j = random.randint(0, len( a ) - 1)
        b.append( a.pop( j ) )
    return b

def random_pic(subdir):
    """Mel8ourne random pic code.
    """
    fileprefix = '/srv/zookeepr/zookeepr/public/random-pix/'
    htmlprefix = '/random-pix/'
    try:
        file = os.path.basename(random.choice(glob(fileprefix + subdir + '/*')))
        return htmlprefix+subdir+'/'+file
    except IndexError:
        return "no images found"

esc_re = re.compile(r'([<>&])')
def esc(s):
    """ HTML-escape the argument"""
    def esc_m(m):
      return {'>': '&gt;', '<': '&lt;', '&': '&amp;'}[m.group(1)]
    if s is None:
      return ''
    try:
      return esc_re.sub(esc_m, s)
    except:
      return esc_re.sub(esc_m, `s`)

break_re = re.compile(r'(\n|\r\n)')
def line_break(s):
    """ Turn line breaks into <br>'s """
    return break_re.sub('<br>', s)

def countries():
    """ list of countries, as retrieved from the miscfiles package
        (stripping of all diacritical marks)
    """
    res = []
    import unicodedata as ud
    for line in gzip.open('/usr/share/misc/countries.gz').readlines():
        if line[0]=='#' or line=='\n':
            continue
        cc = line.split(':')[3].decode('utf8')
        s = ''
        for ch in cc:
            s += ud.normalize('NFD', ch)[0]
        res.append(s)
    res.sort()
    return res

def debug():
    if request_config().environ['paste.config']['global_conf']['debug'] == "true":
        return True
    else:
        return False

teaser_re = re.compile(r'(\<\!\-\-break\-\-\>)')
def make_teaser(body):
    if teaser_re.search(body):
        parts = teaser_re.split(body)
        return parts[0], True
    else:
        return body, False

_news_id = -1
def news_id():
    global _news_id
    if _news_id == -1:
        from sqlalchemy.orm import create_session
        from zookeepr.model import DBContentType
        _news_id = create_session().query(DBContentType).filter_by(name='News').first().id
    return _news_id

def is_news(article_id):
    if news_id() == article_id:
        return True
    return False

computer_re = re.compile(r'([^A-Za-z0-9\_\-])')
def computer_title(title):
    """ Turn a string into a computer friendly tag """
    title = title.replace(' ', '_')
    title = computer_re.sub('', title)
    title = title.lower()
    return title
    

def featured_image(title, big = False):
    """ Returns img src If an image exists in /public/featured/ with the same computer-friendly title as a news item it becomes featured down the left 
    If the image is prefixed with _big_ it becomes the main header feature """
    
    fileprefix = '/home/josh/LCA09/website/db_content/zookeepr/public/featured/'
    htmlprefix = '/featured/'

    
    if big:
        # look for _big_ feature
        if os.path.isdir(fileprefix + computer_title(title)):
            return htmlprefix + computer_title(title) + "/"
        else:
            return False
    else:
        # look for normal
        if os.path.isfile(fileprefix + computer_title(title) + ".png"):
            return htmlprefix + computer_title(title) + ".png"
        else:
            return False
    
    return False
    
