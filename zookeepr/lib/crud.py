#import authkit
#from pylons import Controller, m, h, c, g, session, request, params
#from webhelpers.pagination import paginate
#from sqlalchemy import create_session
#from sqlalchemy.exceptions import SQLError

# FIXME: Find somewhere to document the class attributes used by the generics.

from formencode import Invalid
from pylons import c, h, m, request
from sqlalchemy import create_session

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
        defaults = m.request_args

        new_object = self.model()
        if request.method == 'POST' and defaults:
            result, errors = self.validators['new'].validate(defaults)

            print "result is", result

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
        
        m.subexec('%s/new.myt' % model_name, defaults=defaults, errors=errors)


# class Modify(IdHandler):

# #     def new(self):
# #         """Create a new object.

# #         GET requests will return a blank form for submitting all
# #         attributes.

# #         POST requests will create the object, and return a redirect to
# #         view the new object.
# #         """
# #         # create new session
# #         session = create_session()

# #         # Get the name we refer to the model by
# #         model_name = self.individual
# #         errors = {}
# #         # instantiate a new model object
# #         new_data = self.model()

# #         if request.method == 'POST' and m.errors is None:
# #             # update this new model object with the form data
# #             for k in m.request_args[model_name]:
# #                 setattr(new_data, k, m.request_args[model_name][k])
# #             session.save(new_data)
# #             e = False
# #             try:
# #                 session.flush()
# #             except SQLError, e:
# #                 # How could this have happened? We suck and for now assume
# #                 # it could only happen by it being a duplicate
# #                 m.errors = e
# #                 e = True
# #             if not e:
# #                 session.close()

# #                 default_redirect = dict(action='view', id=self._oid(new_data))
# #                 return self.redirect_to('new', default_redirect)

# #         # assign to the template global
# #         setattr(c, model_name, new_data)

# #         session.close()
# #         # call the template
# #         if m.errors:
# #             print "ERRORS", m.errors
# #             if hasattr(m.errors, 'unpack_errors'):
# #                 print "ERRORS UNPACKED", m.errors.unpack_errors()
# #         c.errors = m.errors
# #         m.subexec('%s/new.myt' % model_name)

# #     new.permissions = authkit.permissions(signed_in=True)

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
        
        if request.method == 'POST' and m.errors is None:
            # update the object with the posted data
            for k in m.request_args[model_name]:
                setattr(obj, k, m.request_args[model_name][k])

            session.save(obj)

            e = False
            try:
                session.flush()
            except SQLError, e:
                # how could this have happened? we suck and for now assume
                # that it could only happen by it being a duplicate
                # p.s. benno sucks
                m.errors = e
                e = True
            if not e:
                session.close()
                return h.redirect_to(action='view', id=self.identifier(obj))

        # assign to the template global
        setattr(c, model_name, obj)
        # call the template
        m.subexec('%s/edit.myt' % model_name)
        
#     edit.permissions = authkit.permissions(signed_in=True)

class Delete(CRUDBase):
    def delete(self, id):
        """Delete the submission type

        GET will return a form asking for approval.

        POST requests will delete the item.
        """
        
        session = create_session()
        
        obj = self.get_obj(id, session)

        if obj is None:
            m.abort(404, "Computer says no")
        
        if request.method == 'POST':
            session.delete(obj)
            session.flush()
            return h.redirect_to(action='index', id=None)

        session.close()
        
        # get the model name
        model_name = self.individual
        # call the template
        m.subexec('%s/confirm_delete.myt' % model_name)

#    delete.permissions = authkit.permissions(signed_in=True)


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
        m.subexec('%s/list.myt' % model_name)

#     index.permissions = authkit.permissions(signed_in=True)

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
        m.subexec('%s/view.myt' % self.individual)

#     view.permissions = authkit.permissions(signed_in=True)

# legacy classes
class View(Read, List):
    pass

class Modify(Create, Update, Delete):
    pass


__all__ = ['Create', 'Read', 'Update', 'Delete', 'List',
           'View', 'Modify',
           ]
