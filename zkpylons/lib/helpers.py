"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
# Import helpers as desired, or define your own, ie:
#from webhelpers.html.tags import checkbox, password

from webhelpers.html import escape, HTML, literal, url_escape
from webhelpers.html.tags import *
from webhelpers.text import *
import webhelpers.constants
from datetime import datetime
import simplejson as json
import markupsafe

try:
    from webhelpers.pylonslib import secure_form
except:
    from webhelpers.html.secure_form import secure_form

from lxml.html.clean import Cleaner

import webhelpers.util as util

from routes import request_config
from routes.util import url_for as pylons_url_for
from pylons import url

from pylons import config, request, session

import os.path, random, array

from zkpylons.lib import auth

from zkpylons.model import Person
from zkpylons.model.config import Config

from zkpylons.config.zkpylons_config import get_path

from sqlalchemy.orm.util import object_mapper

import itertools, re, Image
from glob import glob

from pylons.controllers.util import redirect
from zkpylons.model import meta

# Use locale to provide comma grouped currency values
import locale

def iterdict(items):
    """
    Create a dictionary having a list of items and an iterator to cycle
    through them.

    This is a helper function for cycle() (below).
    """
    return dict(items=items, iter=itertools.cycle(items))

def cycle(*args, **kargs):
    """
    Return the next cycle of the given list.

    Everytime ``cycle`` is called, the value returned will be the next.
    item in the list passed to it. This list is reset on every request,.
    but can also be reset by calling ``reset_cycle()``.

    You may specify the list as either arguments, or as a single list.
    argument.

    This can be used to alternate classes for table rows::

        # In Myghty...
        % for item in items:
        <tr class="<% cycle("even", "odd") %>">
            ... use item ...
        </tr>
        % #endfor

    You can use named cycles to prevent clashes in nested loops. You'll
    have to reset the inner cycle, manually::

        % for item in items:
        <tr class="<% cycle("even", "odd", name="row_class") %>
            <td>
        %     for value in item.values:
                <span style="color:'<% cycle("red", "green", "blue",
                                             name="colors") %>'">
                            item
                </span>
        %     #endfor
            <% reset_cycle("colors") %>
            </td>
        </tr>
        % #endfor
    """
    if len(args) > 1:
        items = args
    else:
        items = args[0]
    name = kargs.get('name', 'default')
    cycles = request_config().environ.setdefault('railshelpers.cycles', {})

    cycle = cycles.setdefault(name, iterdict(items))

    if cycles[name].get('items') != items:
        cycle = cycles[name] = iterdict(items)
    return cycle['iter'].next()

def email_link_to(addr, text=None):
    """ Generate an email link

    Renders a HTML link to an email address.
    Optionally takes a text field which will be used for the text of the
    anchor, otherwise the email address is used.
    """
    return link_to(text if text != None else addr, 'mailto:' + addr)

rot_26 = "rot_13" #used for being sneaky in the tag hashing for LCA2012

def slideshow(set, small=None):
    """
    Generate a slideshow of a set of images, randomly selecting one to
    show first, unless a file is specified.
    """
    try:
        if small == None or small == "":
            # Randomly select a smaller image, set the width of the div to be
            # the width of image.
            small = random.choice(glob(get_path('public_path') + "/images/" + set + "/small/*"))
        else:
            small = get_path('public_path') + "/images/" + set + "/small/" + small

        output = "<div class=\"slideshow\" id=\"%s\" style=\"width: %dpx\">" % (set, int(Image.open(small).size[0]))
        small = os.path.basename(small)

        # Optionally load up some captions for the images.
        caption = dict()
        caption_file = get_path('public_path') + "/images/" + set + "/captions"
        if os.path.exists(caption_file):
            file = open(caption_file, 'r')
            captions = file.readlines()

            # Assign captions to a lookup table
            for cap in captions:
                str = cap.partition(':')
                caption[str[0]] = str[2]

        # Load up all the images in the set directory.
        files = glob(get_path('public_path') + "/images/" + set + '/*')
        for file in files:
            if os.path.isfile(file):
                short_file = os.path.basename(file)
                if short_file == 'captions':
                    continue

                output += "<a href=\"" + get_path('public_html') + "/images/" + set + "/" + short_file + "\" rel=\"lightbox[" + set + "]\""
                if short_file in caption:
                    output += " title=\"" + caption[short_file] + "\""
                output += ">"

                # If we're looking at the small one we've picked, display
                # it as well.
                if short_file == small:
                    output += "<img src=\"" +  get_path('public_html') + "/images/" + set + "/small/" + short_file + "\">"

                    # If there are more than one image in the slideshow
                    # then also display "more...".
                    if files.__len__() > 1:
                        output += '<div class="more">More images...</div>'
                output += "</a>\n";
        output += "</div>\n"
        return output

    except IndexError:
        return "no images found"


break_re = re.compile(r'(\n|\r\n)(?!\s*<(li|ul|ol)>)')
def line_break(text):
    """ Turn line breaks into <br>'s """
    return break_re.sub('<br />', text)

def yesno(value):
    """ Display a read-only checkbox for the value provided """
    if value:
        return markupsafe.Markup('&#9745;')
    else:
        return markupsafe.Markup('&#9744;')

def countries():
    """ list of countries
    """

    # FIXME we should probably store the country codes rather than the country names
    # http://pylonshq.com/docs/en/0.9.7/thirdparty/webhelpers/constants/
    lines = webhelpers.constants.country_codes()
    res = []
    for line in lines:
        country = line[1]
        res.append(country)
    res.sort()
    return res

def debug():
    return config['pylons.errorware']['debug']

teaser_re = re.compile(r'(\<\!\-\-break\-\-\>)')
def make_teaser(body):
    """
    Split an article into a 'teaser' line and the rest of the article,
    on the <!--break--> in the body.  Used in lists of news items.
    """
    if teaser_re.search(body):
        parts = teaser_re.split(body)
        return parts[0], True
    else:
        return body, False

def remove_teaser_break(body):
    """
        Remove the <!--break--> 'teaser' line from an article body.
    """
    if teaser_re.search(body):
        return teaser_re.sub('', body)
    else:
        return body

computer_re = re.compile(r'([^A-Za-z0-9\_\-])')
def computer_title(title):
    """ Turn a string into a computer friendly tag """
    title = title.replace(' ', '_')
    title = computer_re.sub('', title)
    title = title.lower()
    return title

def wiki_link(title):
    """ Turn a string into a wiki friendly tag """
    parts = title.split(' ')
    title = ''.join([part.title() for part in parts])
    title = computer_re.sub('', title)
    return title

def featured_image(title, big = False):
    """
    Returns img src If an image exists in /public/featured/ with the same
    computer-friendly title as a news item it becomes featured down the left If
    big == True then find a directory
    """

    fileprefix = get_path('news_fileprefix')
    htmlprefix = get_path('news_htmlprefix')

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

domain_re = re.compile('^(http:\/\/|ftp:\/\/)?(([a-z]+[a-z0-9]*[\.|\-]?[a-z]+[a-z0-9]*[a-z0-9]+){1,4}\.[a-z]{2,4})')
def domain_only(url):
    """ Truncates a url to the domain only. For use with "in the press" """
    match = domain_re.match(url)
    if match:
        return match.group(2)
    else:
        return url

def extension(name):
    """ Return the extension of a file name"""
    return name.split('.')[-1]

def silly_description():
    adverb    = random.choice(Config.get('silly_description', category='rego')['adverbs'])
    adjective = random.choice(Config.get('silly_description', category='rego')['adjectives'])
    noun      = random.choice(Config.get('silly_description', category='rego')['nouns'])
    start     = random.choice(Config.get('silly_description', category='rego')['starts'])
    if start == 'a' and adverb[0] in ['a', 'e', 'i', 'o', 'u']:
        start = 'an'
    desc = '%s %s %s %s' % (start, adverb, adjective, noun)
    descChecksum = silly_description_checksum(desc)
    return desc, descChecksum

def silly_description_checksum(desc):
    import hashlib, math
    haiku = "Come to Ballarat"\
          "LCA Under the stars"\
          "Comets is landing..."

    #This is meant to be difficult to read, no telling me its indistinguishable from my normal code - Josh
    def fun(cion):
        e = 0.0
        a = 4.1963944517268459E+00
        b = -5.5753297516829114E+00
        c = 2.7916995626938470E+00
        d = -6.5696680861318413E-01
        f = 7.2840990594877031E-02
        g = -3.0390408978587477E-03

        e = g
        e = e * cion + f
        e = e * cion + d
        e = e * cion + c
        e = e * cion + b
        e = e * cion + a
        e = 1.0 / e
        return e

    false = ""
    true = False
    for ny in range(1,9):
        if (ny == 5) or (ny == 8):
            false=false+(haiku[int(math.floor(fun(ny)+1))],haiku[int(math.ceil(fun(ny)+1))])[true]
        else:
            false=false+(haiku[int(math.floor(fun(ny)))],haiku[int(math.ceil(fun(ny)))])[true]
        true = not true
    false=false.lower()+"("+")"

    # Some assistance provided here. All we're doing is taking the silly input string and hashing it with some mysterious salt. Mmmmmm salt
    salted = desc + haiku+eval(false+chr(0x5B)+chr(0x31)+chr(0x5D)).encode(rot_26)
    return  hashlib.sha1(salted.encode('latin1')).hexdigest()

def ticket_percentage_text(percent, earlybird = False):
    if percent == 100:
        return 'All tickets gone.'
    elif percent >= 97.5:
        if earlybird:
            return "Earlybird almost soldout."
        else:
            return "Almost all tickets gone."
    else:
        if earlybird:
            return "%d%% earlybird sold." % percent
        else:
            return "%d%% tickets sold." % percent

link_re = re.compile(r'\[url\=((http:\/\/|ftp:\/\/)?(([a-z]+[a-z0-9]*[\.|\-]?[a-z]+[a-z0-9]*[a-z0-9]+){1,4}\.[a-z]{2,4})([^ \t\n]+))\](.*)\[\/url\]')
def url_to_link(body):
    """ Converts [url=http://example.com]site[/url] into <a href="http://www.example.com">site</a>> """
    return link_re.sub(r'<a href="\1" title="\1">\6</a>', body)

def signed_in_person():
    email_address = request.environ.get("REMOTE_USER")
    if email_address is None:
        return None

    person = Person.find_by_email(email_address, True)
    return person

def object_to_defaults(object, prefix):
    defaults = {}

    for key in object_mapper(object).columns.keys():
        value = getattr(object, key)
        if type(value) == list:
            for code in value:
                defaults['.'.join((prefix, key, code))] = 1
            defaults['.'.join((prefix, key))] = ','.join(value)
        elif value == True:
            defaults['.'.join((prefix, key))] = 1
        else:
            defaults['.'.join((prefix, key))] = value

    return defaults

def check_flash():
    """If the session data isn't of the particular format python has trouble.
    So we check that it is a dict."""
    if session.has_key('flash'):
        if type(session['flash']) != dict:
            del session['flash']
            session.save()

def get_flashes():
    check_flash()
    if not session.has_key('flash'):
        return None
    messages = session['flash']
    # it is save to delete now
    del(session['flash'])
    session.save()
    return messages

def flash(msg, category="information"):
    check_flash()
    if not session.has_key('flash'):
        session['flash'] = {}
    if not session['flash'].has_key(category):
        session['flash'][category] = []
    # If we are redirected we may flash this more than once. Check
    # the message hasn't already been set by looking in the session
    if msg not in session['flash'][category]:
        session['flash'][category].append(msg)
    session.save()

def zk_root():
    """ Helper function to return the root directory of zkpylons,
    this allows completely relevant URL's """
    pass #TODO

def integer_to_currency(number, unit='$', precision=2, divisor=100.0):
    return number_to_currency(number / divisor, unit, precision)

def number_to_currency(number, unit='$', precision=2):
    "Provide an Australian currency version of your number"
    locale.setlocale(locale.LC_ALL, '')
    format_string = "%%.%df" % precision
    return unit + locale.format(format_string, number, grouping=True)

def number_to_percentage(number):
    return str(number) + '%'

def sales_tax(amount):
    """ Calculate the sales tax that for the supplied amount. """
    if Config.get('sales_tax_multiplier') != "":
        sales_tax = int(amount * Config.get('sales_tax_multiplier'))
    elif Config.get('sales_tax_divisor') != "":
        sales_tax = int(amount / Config.get('sales_tax_divisor'))
    else:
        # wtf?
        sales_tax = 0

    return sales_tax

def latex_clean(str):
    """ Sanitise a string suitable for use in LaTeX. """
    str = str.replace('_', '\_')
    str = str.replace('<', '$<$')
    str = str.replace('>', '$>$')
    str = str.replace('&lt;', '$<$')
    str = str.replace('&gt;', '$>$')
    str = str.replace('&', '\&')
    str = str.replace('C#', 'C\#')
    str = re.sub('"(.*?)"', "``\\1''", str)
    str = re.sub('<b>(.*?)</b>', '\\\\textbf{\\1}', str)
    str = re.sub('<i>(.*?)</i>', "\emph{\\1}", str)
    str = re.sub('<ol(.*?)>', '\\\\begin{enumerate}\n', str)
    str = str.replace('</ol>', '\end{enumerate}\n')
    str = str.replace('<ul>', '\\begin{itemize}\n')
    str = str.replace('</ul>', '\end{itemize}\n')
    str = str.replace('<li>', '\item ')
    str = str.replace('</li>', '')
    str = str.replace('<pre>', '\\begin{verbatim}')
    str = str.replace('</pre>', '\end{verbatim}')
    str = str.replace('$', '\$')
    str = str.replace('<div>', '')
    str = str.replace('</div>', '')
    str = str.replace('<p>', '')
    str = str.replace('</p>', '')

    return str

def html_clean(str):
    """ Clean up HTML to be safe """
    cleaner = Cleaner(safe_attrs_only=True)
    return cleaner.clean_html(str)


def redirect_to(*args, **kargs):
    if 'is_active' in dir(meta.Session):
        meta.Session.flush()
        # Close causes issues if we are running under a test harness
        # Not ideal to change behaviour under test but can't see a way around it
        if meta.Session.get_bind().url.database != 'zktest':
            meta.Session.close()

    return redirect(url.current(*args, **kargs))

def url_for(*args, **kwargs):
    fields = dict(request.GET)
    if fields.has_key('hash') and 'hash' not in kwargs:
        kwargs['hash'] = fields['hash']
    return pylons_url_for(*args, **kwargs)


def full_url_for(*args, **kwargs):
    return os.path.join(Config.get('event_permalink'), url_for(*args, **kwargs))


def list_to_string(list, primary_join='%s and %s', secondary_join=', ', html = False):
    if html:
        list = [escape(item) for item in list]
    if len(list) == 0:
        list = ''
    elif len(list) == 1:
        list = list[0]
    else:
        list = primary_join % (secondary_join.join(list[: -1]), list[-1])
    return list

def check_for_incomplete_profile(person):
    if not person.firstname or not person.lastname or not person.i_agree or (Config.get('personal_info', category='rego')['home_address'] == 'yes' and (not person.address1 or not person.city or not person.postcode)):
        if not session.get('redirect_to', None):
            session['redirect_to'] =  request.path_info
            session.save()
        redirect_to(controller='person', action='finish_signup', id=person.id)
