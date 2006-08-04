#from webhelpers.pagination import paginate
#from sqlalchemy import create_session
#from sqlalchemy.exceptions import SQLError

# FIXME: Find somewhere to document the class attributes used by the generics.

from formencode import Invalid
from sqlalchemy import create_session

from zookeepr.lib.base import *

class CRUDBase(object):
    def identifier(self, obj):
        """Return the unique identifier for this model object.
        """
        field_name = getattr(self, 'key', 'id')
        oid = getattr(obj, field_name)
        if oid is None:
            return obj.id
        else:
            return oid
        
    def get_obj(self, id, session):
        use_oid = False # Determines if we look up on a key or the OID
        obj = None

        # If we can convert this to an integer then we look up based on the OID
        try:
            id = int(id)
            use_oid = True
        except ValueError:
            pass

        # get the name we're referring this object to by from the model
        model_name = self.individual

        if use_oid:
            obj = session.get(self.model, id)
        elif hasattr(self, 'key'):
            query_dict = {self.key: id}
            os = session.query(self.model).select_by(**query_dict)
            if len(os) == 1:
                obj = os[0]

        return obj

    def redirect_to(self, action, default):
        """Redirect to the preferred controller/action target.

        Used to redirect the browser after a successful POST.
    
        If ``self`` has an attribute ``redirect_map``, then that is used as
        a map to look up the destination for the redirect for this ``action``.

        If the ``redirect_map`` doesn't exist, or has no preference for
        the current ``action``, then the ``default`` target is used instead.

        The values of the ``redirect_map``, and ``default``, should be a
        dictionary of arguments as one would normally pass to the
        ``h.redirect_to`` call from WebHelpers.
        """
        if hasattr(self, 'redirect_map') and action in self.redirect_map:
            redirect_args = self.redirect_map[action]
        else:
            redirect_args = default
        return h.redirect_to(**redirect_args)
    

class Create(CRUDBase):
    def new(self):
        """Create a new object.

        GET requests will return a blank for for submitting all attributes.

        POST requests will create the object, if the validators pass.
        """
        session = create_session()

        model_name = self.individual
        errors = {}
        defaults = dict(request.POST)

        new_object = self.model()
        if request.method == 'POST' and defaults:
            result, errors = self.validators['new'].validate(defaults)

            if not errors:
                # update the new object with the form data
                for k in result[model_name]:
                    setattr(new_object, k, result[model_name][k])
        
                session.save(new_object)
                session.flush()
                session.close()

                default_redirect = dict(action='view', id=self.identifier(new_object))
                return self.redirect_to('new', default_redirect)

        # make new_object accessible to the template
        setattr(c, model_name, new_object)

        session.close()

        # unmangle the errors
        good_errors = {}
        for key in errors.keys():
            try:
                for subkey in errors[key].keys():
                    good_errors[key + "." + subkey] = errors[key][subkey]
            except AttributeError:
                good_errors[key] = errors[key]

        return render_response('%s/new.myt' % model_name, defaults=defaults, errors=good_errors)


class Update(CRUDBase):
    def edit(self, id):
        """Allow editing of an object.

        GET requests return an 'edit' form, prefilled with the current
        data.

        POST requests update the object with the data posted.
        """
        session = create_session()
        obj = self.get_obj(id, session)

        if obj is None:
            raise "cannot edit nonexistent object for id = '%s'" % (id,)

        # get the name we refer to it by
        model_name = self.individual

        errors = {}
        defaults = dict(request.POST)
        
        if request.method == 'POST' and defaults:
            result, errors = self.validators['edit'].validate(defaults)

            if not errors:
                
                # update the object with the posted data
                for k in result[model_name]:
                    setattr(obj, k, result[model_name][k])

                session.save(obj)
                session.flush()
                session.close()
                
                return h.redirect_to(action='view', id=self.identifier(obj))

        # assign to the template global
        setattr(c, model_name, obj)
        # call the template
        return render_response('%s/edit.myt' % model_name, defaults=defaults, errors=errors)
        

class Delete(CRUDBase):
    def delete(self, id):
        """Delete the submission type

        GET will return a form asking for approval.

        POST requests will delete the item.
        """
        
        session = create_session()
        
        obj = self.get_obj(id, session)

        if obj is None:
            abort(404, "Computer says no")
        
        if request.method == 'POST':
            session.delete(obj)
            session.flush()
            redirect_to(action='index', id=None)

        session.close()
        
        # get the model name
        model_name = self.individual
        # call the template
        return render_response('%s/confirm_delete.myt' % model_name)


class List(CRUDBase):
    def _can_edit(self):
        return issubclass(self.__class__, Modify)
    
    def index(self):
        """Show a list of all objects currently in the system."""
        # GET, POST -> return list of objects

        session = create_session()

        # get name we refer to the model by in the controller
        model_name = self.individual
        
        #options = getattr(self, 'conditions', {})
        #pages, collection = paginate(object_mapper(self.model), m.request_args.get('page', 0), **options)
        #setattr(c, model_name + '_pages', pages)
        #setattr(c, model_name + '_collection', collection)

        # assign list of objects to template global
        setattr(c, model_name + '_collection', session.query(self.model).select())

        session.close()
        
        c.can_edit = self._can_edit()
        # exec the template
        return render_response('%s/list.myt' % model_name)


class Read(CRUDBase):
    def view(self, id):
        """View a specific object"""
        session = create_session()
        obj = self.get_obj(id, session)
        
        if obj is None:
            raise "cannot view nonexistent object for id = '%s'" % (id,)

        # assign to the template global
        setattr(c, self.individual, obj)
        c.can_edit = self._can_edit()

        # exec the template
        return render_response('%s/view.myt' % self.individual)


# legacy classes
class View(Read, List):
    pass

class Modify(Create, Update, Delete):
    pass


__all__ = ['Create', 'Read', 'Update', 'Delete', 'List',
           'View', 'Modify',
           ]
