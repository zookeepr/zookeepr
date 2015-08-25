from mako import exceptions
from mako.template import Template
from mako.runtime import Context
from mako.lookup import TemplateLookup
from StringIO import StringIO
from collections import namedtuple
import re

# Original setup

lca_menu = [
  ('Home', '/', 'home'),
  ('About', '/about/linux.conf.au', 'about'),
  ('Brisbane', '/brisbane/about', 'brisbane'),
  ('Sponsors', '/sponsors/sponsors', 'sponsors'),
  ('Programme', '/programme/about', 'programme'),
  ('Register', '/register/prices', 'register'),
  ('Media', '/media/news', 'media'),
  ('Contact', '/contact', 'contact'),
  ('Wiki page', '/wiki', 'wiki'),
]

lca_submenus = {
  'about': ['linux.conf.au', 'lca2011 Ninjas', 'Venue', 'History', 'Linux/Open Source', 'Harassment'],
  'brisbane': ['About', 'Sightseeing'],
  'sponsors': ['Sponsors', 'Why Sponsor'],
  'programme': ['About', 'Keynotes', 'Miniconfs', 'Schedule', 'Social Events', 'Open Day', 'Partners Programme'], # stage 3
  'register': ['Prices', 'Accommodation', 'Terms and Conditions'],
  'media': ['News','In the press','Graphics']
}

lookup = TemplateLookup(directories=['zkpylons/templates/'])
t = Template("""
        <%include file="/nav.mako" />
        <%include file="/subnav.mako" />
        <%include file="/subsubnav.mako" />
""", lookup=lookup)
test_url = '/'
def get_test_url():
    return test_url
helper_struct = namedtuple('helper', 'lca_menu lca_submenus url_for')
context_struct = namedtuple('context', 'subsubmenu')

def gen_nav(url):
    global test_url
    test_url = url

    h = helper_struct(lca_submenus=lca_submenus, lca_menu=lca_menu, url_for=get_test_url)
    c = context_struct(subsubmenu = {})
    buf = StringIO()
    ctx = Context(buf, h=h, c=c)

    try:
        t.render_context(ctx)
        full_html = buf.getvalue()
    except:
        print exceptions.text_error_template().render()
        return

    full_html = buf.getvalue()
    sub_html_pt = full_html.find("<!-- Secondary navigation")
    pri_html = full_html[0:sub_html_pt]
    sec_html = full_html[sub_html_pt:-1]

    pri_text = [y for y in (x.strip() for x in re.sub(r'<.*?>', '', pri_html).splitlines()) if y]
    sec_text = [y for y in (x.strip() for x in re.sub(r'<.*?>', '', sec_html).splitlines()) if y]

    # put a flag "LINK" in each line with a url, strip it out later
    mangled_pri_links = re.sub(r'.*?href\s?=\s?[\'"](.*?)[\'"].*', r'LINK \1', pri_html)
    pri_links = [x[5:].strip() for x in mangled_pri_links.splitlines() if x[0:5] == "LINK "]
    mangled_sec_links = re.sub(r'.*?href\s?=\s?[\'"](.*?)[\'"].*', r'LINK \1', sec_html)
    sec_links = [x[5:].strip() for x in mangled_sec_links.splitlines() if x[0:5] == "LINK "]

    return {'full_html':full_html, 'pri_text':pri_text, 'pri_links':pri_links, 'sec_text':sec_text, 'sec_links':sec_links}


print ""
print gen_nav('/')['sec_text']
print gen_nav('/about/linux.conf.au')['sec_text']
print gen_nav('/programme/about')['sec_text']
