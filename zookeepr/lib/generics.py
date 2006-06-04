import authkit
from pylons import Controller, m, h, c, g, session, request, params
#from webhelpers.pagination import paginate
from sqlalchemy import create_session
from sqlalchemy.exceptions import SQLError

class IdHandler(object):
    def _oid(self, obj):
        """Return the ID for the model."""
        field_name = getattr(self, 'key', 'id')
        oid = getattr(obj, field_name)
        if oid is None:
            return obj.id
        else:
            return oid

    def get_obj(self, id):
        use_oid = False # Determines if we look up on a key or the OID
        obj = None

        # If we can convert this to an integer then we look up based on the OID
        try:
            id = int(id)
            use_oid = True
        except ValueError:
            pass

        session = create_session()

        # get the name we're referring this object to by from the model
        model_name = self.individual

        if use_oid:
            obj = session.get(self.model, id)
        elif hasattr(self, 'key'):
            query_dict = {self.key: id}
            os = session.query(self.model).select_by(**query_dict)
            if len(os) == 1:
                obj = os[0]

        return obj, session

class Modify(IdHandler):

    def new(self):
        """Create a new object.

        GET requests will return a blank form for submitting all
        attributes.

        POST requests will create the object, and return a redirect to
        view the new object.
        """
        # create new session
        session = create_session()

        # Get the name we refer to the model by
        model_name = self.individual
        errors = {}
        # instantiate a new model object
        new_data = self.model()

        if request.method == 'POST' and m.errors is None:
            # update this new model object with the form data
            for k in m.request_args[model_name]:
                setattr(new_data, k, m.request_args[model_name][k])
            session.save(new_data)
            e = False
            try:
                session.flush()
            except SQLError, e:
                # How could this have happened? We suck and for now assume
                # it could only happen by it being a duplicate
                m.errors = e
                e = True
            if not e:
                session.close()
                return h.redirect_to(action='view', id=self._oid(new_data))

        # assign to the template global
        setattr(c, model_name, new_data)

        session.close()
        # call the template
        if m.errors:
            print "ERRORS", m.errors
            if hasattr(m.errors, 'unpack_errors'):
                print "ERRORS UNPACKED", m.errors.unpack_errors()
        c.errors = m.errors
        m.subexec('%s/new.myt' % model_name)

    new.permissions = authkit.permissions(signed_in=True)
        
    def edit(self, id):
        """Allow editing of an object.

        GET requests return an 'edit' form, prefilled with the current
        data.

        POST requests update the object with the data posted.
        """
        obj, session = self.get_obj(id)

        if obj is None:
            raise "Badness"

        # get the name we refer to it by
        model_name = self.individual
        
        if request.method == 'POST' and m.errors is None:
            # update the object with the posted data
            for k in m.request_args[model_name]:
                setattr(obj, k, m.request_args[model_name][k])

            session.save(obj)

            print "saving"
            
            e = False
            try:
                session.flush()
            except SQLError, e:
                # how could this have happened? we suck and for now assume
                # that it could only happen by it being a duplicate
                # p.s. benno sucks
                m.errors = e
                e = True

        session.close()
        # assign to the template global
        setattr(c, model_name, obj)
        # call the template
        m.subexec('%s/edit.myt' % model_name)
        
    edit.permissions = authkit.permissions(signed_in=True)
    
    def delete(self, id):
        """Delete the submission type

        GET will return a form asking for approval.

        POST requests will delete the item.
        """
        obj, session = self.get_obj(id)
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

    delete.permissions = authkit.permissions(signed_in=True)

class View(object):
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

    index.permissions = authkit.permissions(signed_in=True)
    
    def view(self, id):
        """View a specific object"""
        obj, session = self.get_obj(id)
        
        if obj is None:
            raise "Badness"

        # assign to the template global
        setattr(c, self.individual, obj)
        c.can_edit = self._can_edit()

        # exec the template
        m.subexec('%s/view.myt' % self.individual)

    view.permissions = authkit.permissions(signed_in=True)
