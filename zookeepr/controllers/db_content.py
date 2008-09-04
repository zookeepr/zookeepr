import logging
from formencode import validators, variabledecode
from formencode.schema import Schema
from zookeepr.lib.base import *
from zookeepr.lib.auth import *
from zookeepr.lib.crud import *
from zookeepr.lib.validators import BaseSchema, BoundedInt, DbContentTypeValidator
from zookeepr.lib.base import *
from zookeepr.controllers import not_found
from zookeepr.model.db_content import DBContentType
from pylons import response
from zookeepr.config.lca_info import file_paths
import os
import cgi

from webhelpers.pagination import paginate

log = logging.getLogger(__name__)

class DbContentSchema(BaseSchema):
    title = validators.String(not_empty=True)
    type = DbContentTypeValidator()
    url = validators.String()
    body = validators.String()

class NewContentSchema(BaseSchema):
    db_content = DbContentSchema()
    pre_validators = [variabledecode.NestedVariables]

class UpdateContentSchema(BaseSchema):
    db_content = DbContentSchema()
    pre_validators = [variabledecode.NestedVariables]

class DbContentController(SecureController, Create, List, Read, Update, Delete):
    individual = 'db_content'
    model = model.DBContent
    schemas = {'new': NewContentSchema(),
               'edit': UpdateContentSchema()
              }

    permissions = {'new': [AuthRole('organiser')],
                   'index': [AuthRole('organiser')],
                   'page': True,
                   'view': True,
                   'edit': [AuthRole('organiser')],
                   'delete': [AuthRole('organiser')],
                   'list_news': True,
                   'list_press': True,
                   'rss_news': True,
                   'upload': [AuthRole('organiser')],
                   'list_files': [AuthRole('organiser')],
                   'delete_file': [AuthRole('organiser')],
                   'delete_folder': [AuthRole('organiser')],
                   }

    def __before__(self, **kwargs):
        super(DbContentController, self).__before__(**kwargs)
        c.db_content_types = self.dbsession.query(DBContentType).all()

    def view(self):
        news_id = self.dbsession.query(model.DBContentType).filter_by(name='News').first().id
        c.is_news = False
        if news_id == c.db_content.type_id:
            c.is_news = True
        return super(DbContentController, self).view()

    def page(self):
        url = h.url()()
        if url[0]=='/': url=url[1:]
        c.db_content = self.dbsession.query(model.DBContent).filter_by(url=url).first()
        if c.db_content is not None:
            return self.view()
        return not_found.NotFoundController().view()

    def list_news(self):
        news_id = self.dbsession.query(model.DBContentType).filter_by(name='News').first().id
        news_list = self.dbsession.query(self.model).filter_by(type_id=news_id).order_by(self.model.c.creation_timestamp.desc()).all()
        pages, collection = paginate(news_list, per_page = 20)
        setattr(c, self.individual + '_pages', pages)
        setattr(c, self.individual + '_collection', collection)
        return render_response('%s/list_news.myt' % self.individual)

    def rss_news(self):
        news_id = self.dbsession.query(model.DBContentType).filter_by(name='News').first().id
        news_list = self.dbsession.query(self.model).filter_by(type_id=news_id).order_by(self.model.c.creation_timestamp.desc()).limit(20).all()
        setattr(c, self.individual + '_collection', news_list)
        response.headers['Content-type'] = 'application/rss+xml; charset=utf-8'
        return render_response('%s/rss_news.myt' % self.individual, fragment=True)

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

        return render('%s/file_uploaded.myt' % self.individual)

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
                return render('%s/folder_full.myt' % self.individual)
            return render('%s/folder_deleted.myt' % self.individual)
        return render('%s/delete_folder.myt' % self.individual)

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
            return render('%s/file_deleted.myt' % self.individual)
        return render('%s/delete_file.myt' % self.individual)

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
                pass

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
        return render('%s/list_files.myt' % self.individual)

    def list_press(self):
        press_id = self.dbsession.query(model.DBContentType).filter_by(name='In the press').first().id
        press_list = self.dbsession.query(self.model).filter_by(type_id=press_id).order_by(self.model.c.creation_timestamp.desc()).all()
        pages, collection = paginate(press_list, per_page = 20)
        setattr(c, self.individual + '_pages', pages)
        setattr(c, self.individual + '_collection', collection)
        return render_response('%s/list_press.myt' % self.individual)
