import logging

from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on

from formencode import validators, htmlfill
from formencode.variabledecode import NestedVariables

from zookeepr.lib.base import BaseController, render
from zookeepr.lib.validators import BaseSchema, DbContentTypeValidator
import zookeepr.lib.helpers as h

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser

from zookeepr.lib.mail import email

from zookeepr.model import meta
from zookeepr.model import DbContent, DbContentType

from zookeepr.config.lca_info import lca_info
from not_found import NotFoundController

from webhelpers import paginate
from zookeepr.config.lca_info import file_paths
import os

log = logging.getLogger(__name__)

class DbContentSchema(BaseSchema):
    title = validators.String(not_empty=True)
    type = DbContentTypeValidator()
    url = validators.String()
    body = validators.String()

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
        return render('/db_content/new.mako')

    @validate(schema=NewDbContentSchema(), form='new')
    def _new(self):
        results = self.form_result['db_content']
        c.db_content = DbContent(**results)
        meta.Session.add(c.db_content)
        meta.Session.commit()

        h.flash("New Page Created.")
        redirect_to(action='view', id=c.db_content.id)

    def view(self, id):
        c.db_content = DbContent.find_by_id(id)
        return render('/db_content/view.mako')

    def page(self):
        url = h.url_for()
        if url[0]=='/': url=url[1:]
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
        
        form = render('/db_content/edit.mako')
        return htmlfill.render(form, defaults)

    @validate(schema=UpdateDbContentSchema(), form='edit')
    def _edit(self, id):
        c.db_content = DbContent.find_by_id(id)

        for key in self.form_result['db_content']:
            setattr(c.db_content, key, self.form_result['db_content'][key])

        # update the objects with the validated form data
        meta.Session.commit()
        h.flash("Page updated.")
        redirect_to(action='view', id=id)

    @authorize(h.auth.has_organiser_role)
    @dispatch_on(POST="_delete") 
    def delete(self, id):
        c.db_content = DbContent.find_by_id(id)
        return render('/db_content/confirm_delete.mako')

    @validate(schema=None, form='delete')
    def _delete(self, id):
        c.db_content = DbContent.find_by_id(id)
        meta.Session.delete(c.db_content)
        meta.Session.commit()

        h.flash("Content Deleted.")
        redirect_to('index')

    def list_news(self):
        if c.db_content_types:
            pages, collection = paginate.Page(DbContent.find_all_by_type("News"), per_page = 20)
            c.db_content_pages = pages
            c.db_content_collection = collection
            c.result = True
        else:
            c.result = False
        return render('/db_content/list_news.mako')

    def list_press(self):
        if c.db_content_types:
            pages, collection = paginate.Page(DbContent.find_all_by_type("In the press"), per_page = 20)
            c.db_content_pages = pages
            c.db_content_collection = collection
            c.result = True
        else:
            c.result = False
        return render('/db_content/list_press.mako')

    def rss_news(self):
        news_id = DbContentType.find_by_name("News")
        c.db_content_collection = []
        if news_id is not None: 
            c.db_content_collection = meta.Session.query(DbContent).filter_by(type_id=news_id).order_by(DbContent.creation_timestamp.desc()).limit(20).all()
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

        file_data = request.POST['myfile'].value
        fp = open(directory + request.POST['myfile'].filename,'wb')
        fp.write(file_data)
        fp.close()
        
        h.flash("File Uploaded.")        
        redirect_to(action="list_files", folder=c.current_folder)

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
            try:
                os.rmdir(directory + c.folder)
            except OSError:
                h.flash("Can not delete. The folder contains items.", 'error')
                redirect_to(action="list_files", folder=c.current_folder)
            h.flash("Folder deleted.")
            redirect_to(action="list_files", folder=c.current_folder)
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
            redirect_to(action="list_files", folder=c.current_folder)
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
        return render('/db_content/list_files.mako')
