import authkit
from pylons import Controller, m, h, c, g, session, request, params
#from webhelpers.pagination import paginate
from sqlalchemy import create_session

class Modify(object):
    def _oid(self, obj):
        """Return the ID for the model."""
        field_name = getattr(self, 'key', 'id')
        oid = getattr(obj, field_name)
        return oid

#     def get(self, obj, id):
#         if not hasattr(self, 'key'):
#             obj = self.model.get(id)
#         else:
#             objs = self.model.select(getattr(self.model.c, self.key)==id)
#             if len(objs) == 0:
#                 obj = None
#             else:
#                 obj = objs[0]
#         return obj
                                       
        
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

        if request.method == 'POST':

            # update this new model object with the form data
            new_data.update(**m.request_args[model_name])
            
            if new_data.validate():
                #session['message'] = 'Object has been created, now editing.'
                #session.save()
                # save to database
                session.save(new_data)
                session.flush()
                session.close()
                return h.redirect_to(action='edit', id=self._oid(new_data))

        # assign to the template global
        setattr(c, model_name, new_data)
        session.close()
        # call the template
        m.subexec('%s/new.myt' % model_name)

    new.permissions = authkit.permissions(signed_in=True)
        
    def edit(self, id):
        """Allow editing of an object.

        GET requests return an 'edit' form, prefilled with the current
        data.

        POST requests update the object with the data posted.
        """

        # clear the store
        session = create_session()
        
        # Get the object
        obj = session.get(self.model, id)
        if not obj:
            #session['message'] = 'No such id.'
            #session.save()
            return h.redirect_to(action='index', id=None)

        # get the name we refer to it by
        model_name = self.individual
        
        if request.method == 'POST':
            # update the object with the posted data
            obj.update(**m.request_args[model_name])
            
            if obj.validate():
                #session['message'] = 'Object has been updated successfully.'
                session.save(obj)
                session.flush()
            else:
                #session['message'] = 'Object failed to update, errors present.'
                session.clear()

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
        # clear the store
        session = create_session()
        
        # Get the object
        obj = session.get(self.model, id)
        if not obj:
            #session['message'] = 'No such id.'
            #session.save()
            return h.redirect_to(action='index', id=None)
        
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
        # GET, POST -> return subtype

        session = create_session()

        # get the name we're referring this object to by from the model
        model_name = self.individual
        # assign to the template global
        setattr(c, model_name, session.get(self.model, id))
        c.can_edit = self._can_edit()

        session.close()
        
        # exec the template
        m.subexec('%s/view.myt' % model_name)

    view.permissions = authkit.permissions(signed_in=True)
