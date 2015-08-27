from mako import exceptions
from mako.template import Template
from mako.runtime import Context
from mako.lookup import TemplateLookup
from StringIO import StringIO
from collections import namedtuple
import re

lookup = TemplateLookup(directories=['zkpylons/templates/'])
t = Template("""
        <%include file="/nav.mako" />
        <%include file="/subnav.mako" />
        <%include file="/subsubnav.mako" />
""", lookup=lookup)
test_url = '/'
def get_test_url():
    return test_url
helper_struct = namedtuple('helper', 'url_for')
context_struct = namedtuple('context', 'subsubmenu')

def gen_nav(url):
    global test_url
    test_url = url

    h = helper_struct(url_for=get_test_url)
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

    # Find the selected link, if there is one
    pri_sel = [re.sub(r'.*?href\s?=\s?[\'"](.*?)[\'"].*', r'\1',x) for x in pri_html.splitlines() if "selected" in x]
    sec_sel = [re.sub(r'.*?href\s?=\s?[\'"](.*?)[\'"].*', r'\1',x) for x in sec_html.splitlines() if "selected" in x]
    sec_sel_text = [re.sub(r'<.*?>', '', x).strip() for x in sec_html.splitlines() if "selected" in x]

    return {'full_html':full_html, 'pri_text':pri_text, 'pri_links':pri_links, 'sec_text':sec_text, 'sec_links':sec_links, 'pri_sel':pri_sel[0] if pri_sel else None, 'sec_sel':sec_sel[0] if sec_sel else None, 'sec_sel_text':sec_sel_text[0] if sec_sel_text else None}


def test_root_walk():
    """ Start at / and walk through all the nav links testing the structure """

    root = gen_nav('/')
    assert len(root['pri_text']) == len(root['pri_links'])
    assert len(root['sec_text']) == 0
    assert len(root['sec_links']) == 0

    for pri_link in root['pri_links']:
        sub = gen_nav(pri_link)
        # Ensure consistency
        assert sub['pri_sel'] == pri_link
        assert sub['pri_text'] == root['pri_text']
        assert sub['pri_links'] == root['pri_links']
        # Each subheading may have secondary links
        assert len(sub['sec_text']) == len(sub['sec_links'])
        # Subpages should select the primary link
        assert sub['pri_sel'] == pri_link
        # If the current page is present in the subpage list, it should be selected
        # This is does with a "" link
        if "" in sub['sec_links']:
            assert sub['sec_sel'] == ""
            # Can't test for sec_sel_text, unsure what it should be
        assert pri_link not in sub['sec_links']

        for sub_link in sub['sec_links']:
            if(sub_link): # Some links are "" --> this page, skip over them
                sec = gen_nav(sub_link)
                # Ensure consistency
                assert sec['pri_sel'] == pri_link
                assert sec['pri_text'] == root['pri_text']
                assert sec['pri_links'] == root['pri_links']
                assert sec['sec_text'] == sub['sec_text']
                # Link is "" (this page), text should reflect the selected link
                assert sec['sec_sel'] == ""
                assert sec['sec_sel_text'] == sub['sec_text'][sub['sec_links'].index(sub_link)]
