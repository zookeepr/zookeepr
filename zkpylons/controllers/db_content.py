import logging

from pylons import request, response, session, tmpl_context as c
from zkpylons.lib.helpers import redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on

from formencode import validators, htmlfill
from formencode.variabledecode import NestedVariables

from zkpylons.lib.base import BaseController, render
from zkpylons.lib.validators import BaseSchema, DbContentTypeValidator
import zkpylons.lib.helpers as h
from datetime import datetime, timedelta

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser

from zkpylons.lib.mail import email

from zkpylons.model import meta
from zkpylons.model import DbContent, DbContentType

from zkpylons.config.lca_info import lca_info
from not_found import NotFoundController

from webhelpers import paginate
from pylons.controllers.util import abort

from zkpylons.config.zkpylons_config import file_paths

import os
import re

log = logging.getLogger(__name__)

class DbContentSchema(BaseSchema):
    title = validators.String(not_empty=True)
    type = DbContentTypeValidator()
    url = validators.String()
    body = validators.String()
    publish_date = validators.DateConverter(month_style='dd/mm/yyyy')
    publish_time = validators.TimeConverter(use_datetime=True)

class NewDbContentSchema(BaseSchema):
    db_content = DbContentSchema()
    pre_validators = [NestedVariables]

class UpdateDbContentSchema(BaseSchema):
    db_content = DbContentSchema()
    pre_validators = [NestedVariables]


class DbContentController(BaseController):
    def __before__(self, **kwargs):
        c.db_content_types = DbContentType.find_all()

    @authorize(h.auth.has_organiser_role)
    def index(self):
        c.db_content_collection = DbContent.find_all()
        return render('/db_content/list.mako')

    @authorize(h.auth.has_organiser_role)
    @dispatch_on(POST="_new") 
    def new(self):
        if len(c.db_content_types) is 0:
            h.flash("Configuration Error: Please make sure at least one content type exists.", 'error')
        if DbContentType.find_by_name("News") is None:
            h.flash("Configuration Error: Please make sure the 'News' content type exists for full functionality.", 'error')
        if DbContentType.find_by_name("In the press") is None:
            h.flash("Configuration Error: Please make sure the 'In the press' content type exists for full functionality.", 'error')
        c.db_content = DbContent()
        defaults = h.object_to_defaults(c.db_content, 'db_content')
        if request.GET.has_key('url'):
            defaults['db_content.type'] = 1 # This is bad... we're assuming we have #1 as new page
            if request.GET['url'].startswith('/'):
                defaults['db_content.url'] = str(request.GET['url'])[1:]
            else:
                defaults['db_content.url'] = request.GET['url']
        form = render('/db_content/new.mako')
        return htmlfill.render(form, defaults)

    @validate(schema=NewDbContentSchema(), form='new', post_only=True, on_get=True, variable_decode=True)
    def _new(self):
        results = self.form_result['db_content']
        if results['publish_time'] is None:
            results['publish_time'] = datetime.time(datetime.now())
        if results['publish_date'] is not None:
            results['publish_timestamp'] = datetime.combine(results['publish_date'], results['publish_time'])
        else:
            results['publish_timestamp'] = None
        del results['publish_date']
        del results['publish_time']
        
        c.db_content = DbContent(**results)
        meta.Session.add(c.db_content)
        meta.Session.commit()

        h.flash("New Page Created.")
        redirect_to(action='view', id=c.db_content.id)

    # Return the page, if the page is not published, and we're not an
    # organiser, suppress the page.
    def view(self, id):
        c.db_content = DbContent.find_by_id(id)
        if c.db_content.publish_timestamp > datetime.now() and not h.auth.authorized(h.auth.has_organiser_role):
            c.db_content = None
            return NotFoundController().view()
        elif c.db_content.publish_timestamp > datetime.now():
            h.flash(("This content is marked to be published on %s and will not be visiable to public until then." % c.db_content.publish_timestamp), 'Warning')

        if c.db_content.type.name == 'Redirect':
            redirect_to(c.db_content.body.encode("latin1"), _code=301)
	c.html_headers, c.html_body, c.menu_contents = self.parse_dbpage(
            c.db_content.body)
        return render('/db_content/view.mako')

    def page(self):
        url = h.url_for().strip("/")
        c.db_content = DbContent.find_by_url(url, abort_404=False)
        if c.db_content is not None:
           return self.view(c.db_content.id)
        return NotFoundController().view()

    @authorize(h.auth.has_organiser_role)
    @dispatch_on(POST="_edit") 
    def edit(self, id):
        c.db_content = DbContent.find_by_id(id)

        defaults = h.object_to_defaults(c.db_content, 'db_content')
        # This is horrible, don't know a better way to do it
        if c.db_content.type:
            defaults['db_content.type'] = defaults['db_content.type_id']

        defaults['db_content.publish_date'] = c.db_content.publish_timestamp.strftime('%d/%m/%y')
        defaults['db_content.publish_time'] = c.db_content.publish_timestamp.strftime('%H:%M:%S')

        form = render('/db_content/edit.mako')
        return htmlfill.render(form, defaults)

    @validate(schema=UpdateDbContentSchema(), form='edit', post_only=True, on_get=True, variable_decode=True)
    def _edit(self, id):
        c.db_content = DbContent.find_by_id(id)

        for key in self.form_result['db_content']:
            if ( not key in ['publish_date', 'publish_time'] ):
                setattr(c.db_content, key, self.form_result['db_content'][key])

        if self.form_result['db_content']['publish_time'] is None:
            self.form_result['db_content']['publish_time'] = datetime.time(datetime.now())

        if self.form_result['db_content']['publish_date'] is not None:
            c.db_content.publish_timestamp = \
                    datetime.combine(self.form_result['db_content']['publish_date'], \
                                    self.form_result['db_content']['publish_time'])
        else:
            c.db_content.publish_timestamp = datetime.now()


        # update the objects with the validated form data
        meta.Session.commit()
        h.flash("Page updated.")
        redirect_to(action='view', id=id)

    @authorize(h.auth.has_organiser_role)
    @dispatch_on(POST="_delete")
    def delete(self, id):
        c.db_content = DbContent.find_by_id(id)
        return render('/db_content/confirm_delete.mako')

    @validate(schema=None, form='delete', post_only=True, on_get=True, variable_decode=True)
    def _delete(self, id):
        c.db_content = DbContent.find_by_id(id)
        meta.Session.delete(c.db_content)
        meta.Session.commit()

        h.flash("Content Deleted.")
        redirect_to('index')

    def list_news(self):
        if c.db_content_types:
            page = 1
            if request.GET.has_key('page'):
                page = request.GET['page']
            pagination = paginate.Page(DbContent.find_all_by_type("News"), page = page, items_per_page = 10)

            c.db_content_pages = pagination
            c.db_content_collection = pagination.items
            c.result = True
        else:
            c.result = False
        return render('/db_content/list_news.mako')

    def list_press(self):
        if c.db_content_types:
            page = 1
            if request.GET.has_key('page'):
                page = request.GET['page']
            pagination = paginate.Page(DbContent.find_all_by_type("In the press"), page = page, items_per_page = 10)

            c.db_content_pages = pagination
            c.db_content_collection = pagination.items
            c.result = True
        else:
            c.result = False
        return render('/db_content/list_press.mako')

    def rss_news(self):
        news_id = DbContentType.find_by_name("News")
        c.db_content_collection = []
        if news_id is not None: 
            c.db_content_collection = meta.Session.query(DbContent).filter_by(type_id=news_id.id).filter(DbContent.publish_timestamp <= datetime.now()).order_by(DbContent.publish_timestamp.desc()).limit(20).all()
        response.headers['Content-type'] = 'application/rss+xml; charset=utf-8'
        return render('/db_content/rss_news.mako')

    @authorize(h.auth.has_organiser_role)
    def upload(self):
        directory = file_paths['public_path']
        try:
            if request.GET['folder'] is not None:
                directory += request.GET['folder']
                c.current_folder = request.GET['folder']
        except KeyError:
            directory = file_paths['public_path'] + "/"
            c.current_folder = '/'

        if hasattr(request.POST['myfile'], 'value'):
            file_data = request.POST['myfile'].value
            fp = open(directory + request.POST['myfile'].filename,'wb')
            fp.write(file_data)
            fp.close()
            h.flash("File Uploaded.")
        c.no_theme = 'false'
        if request.GET.has_key('no_theme'):
            if request.GET['no_theme'] == 'true':
                c.no_theme = 'true'
        redirect_to(action="list_files", folder=c.current_folder, no_theme=c.no_theme)

    @authorize(h.auth.has_organiser_role)
    def delete_folder(self):
        try:
            if request.GET['folder'] is not None:
                c.folder += request.GET['folder']
                c.current_folder += request.GET['current_path']
        except KeyError:
           abort(404)

        directory = file_paths['public_path']
        defaults = dict(request.POST)
        if defaults:
            c.no_theme = 'false'
            if request.GET.has_key('no_theme'):
                if request.GET['no_theme'] == 'true':
                    c.no_theme = 'true'
            try:
                os.rmdir(directory + c.folder)
            except OSError:
                h.flash("Can not delete. The folder contains items.", 'error')
                redirect_to(action="list_files", folder=c.current_folder, no_theme = c.no_theme)
            h.flash("Folder deleted.")
            redirect_to(action="list_files", folder=c.current_folder, no_theme = c.no_theme)
        c.no_theme = False
        if request.GET.has_key('no_theme'):
            if request.GET['no_theme'] == 'true':
                c.no_theme = True
        return render('/db_content/delete_folder.mako')

    @authorize(h.auth.has_organiser_role)
    def delete_file(self):
        try:
            if request.GET['file'] is not None:
                c.file += request.GET['file']
                c.current_folder += request.GET['folder']
        except KeyError:
           abort(404)

        directory = file_paths['public_path']
        defaults = dict(request.POST)
        if defaults:
            os.remove(directory + c.file)
            h.flash("File Removed")
            c.no_theme = 'false'
            if request.GET.has_key('no_theme'):
                if request.GET['no_theme'] == 'true':
                    c.no_theme = 'true'
            redirect_to(action="list_files", folder=c.current_folder, no_theme = c.no_theme)
        c.no_theme = False
        if request.GET.has_key('no_theme'):
            if request.GET['no_theme'] == 'true':
                c.no_theme = True
        return render('/db_content/delete_file.mako')

    @authorize(h.auth.has_organiser_role)
    def list_files(self):
        # Taken from http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/170242
        def caseinsensitive_sort(stringList):
            """case-insensitive string comparison sort
            doesn't do locale-specific compare
            though that would be a nice addition
            usage: stringList = caseinsensitive_sort(stringList)"""

            tupleList = [(x.lower(), x) for x in stringList]
            tupleList.sort()
            return [x[1] for x in tupleList]

        directory = file_paths['public_path']
        download_path = file_paths['public_html']
        current_path = "/"
        try:
            if request.GET['folder'] is not None:
                directory += request.GET['folder']
                download_path += request.GET['folder']
                current_path = request.GET['folder']
        except KeyError:
            download_path += '/'

        defaults = dict(request.POST)
        if defaults:
            try:
                if request.POST['folder'] is not None:
                    os.mkdir(directory + request.POST['folder'])
            except KeyError:
                h.flash("Error creating folder. Check file permissions.", 'error')
            else:
                h.flash("Folder Created")
            

        files = []
        folders = []
        for filename in os.listdir(directory):
            if os.path.isdir(directory + "/" + filename):
                folders.append(filename + "/")
            else:
                files.append(filename)

        c.file_list = caseinsensitive_sort(files)
        c.folder_list = caseinsensitive_sort(folders)
        c.current_path = current_path
        c.download_path = download_path
        c.no_theme = False
        if request.GET.has_key('no_theme'):
            if request.GET['no_theme'] == 'true':
                c.no_theme = True
        return render('/db_content/list_files.mako')

    HEADER_RE = re.compile("""(?is)\s*<\s*head\s*>\s*(.*?)</\s*head\s*>\s*""")
    FINDH3_RE = re.compile("""(?ism)(<h3>(.+?)</h3>)""")
    NONALPHA_RE = re.compile("""(?s)(\W+)""")
    SLIDESHOW_RE = re.compile("""({{slideshow:\s*(.*?)(,\s*(.*))?}})""")
    @classmethod
    def parse_dbpage(cls, html):
        #
        # Extract stuff at the start of the html between <head>..</head> so
        # it can be hoisted to the page header.
        #
        header_match = cls.HEADER_RE.match(html)
        if not header_match:
            html_headers = ""
            html_body = html
        else:
            html_headers = header_match.group(1)
            html_body = html[header_match.end():]
        #
        # Find headings and make a menu out of them.
        #
        menu_contents = []
        h3 = cls.FINDH3_RE.findall(html_body)
        if h3.__len__() > 0:
            for match in h3:
                simple_title = cls.NONALPHA_RE.sub('', match[1])
                a_element = r'<a name="%s"></a>\g<0>' % (simple_title,)
                html_body = re.compile(match[0]).sub(a_element, html_body)
                li_element = r'<li><a href="#%s">%s</a></li>' % (
                    simple_title, match[1], )
                menu_contents.append(li_element)
        menu_contents = '\n'.join(menu_contents)
        #
        # Build up the slidshow.
        #
        slideshow = cls.SLIDESHOW_RE.findall(html_body)
        if slideshow.__len__() > 0:
            for match in slideshow:
                slideshow_repl = h.slideshow(match[1], match[3])
                html_body = re.compile(match[0]).sub(slideshow_repl, html_body)
        return html_headers, html_body, menu_contents
