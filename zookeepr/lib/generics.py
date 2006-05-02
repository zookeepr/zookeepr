from pylons import Controller, m, h, c, g, session, request, params
#from webhelpers.pagination import paginate
from sqlalchemy import objectstore

class Modify(object):
    def new(self):
        """Create a new object.

        GET requests will return a blank form for submitting all
        attributes.

        POST requests will create the object, and return a redirect to
        view the new object.
        """
        # Get the name we refer to the model by
        model_name = getattr(self, 'individual', self.model.mapper.table.name)
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
                objectstore.flush()
                return h.redirect_to(action='edit', id=new_data.id)

        # assign to the template global
        setattr(c, model_name, new_data)
        # call the template
        m.subexec('%s/new.myt' % model_name)
        
    def edit(self, id):
        """Allow editing of an object.

        GET requests return an 'edit' form, prefilled with the current
        data.

        POST requests update the object with the data posted.
        """
        # Get the object
        obj = self.model.get(id)
        if not obj:
            #session['message'] = 'No such id.'
            #session.save()
            return h.redirect_to(action='index', id=None)

        # get the name we refer to it by
        model_name = getattr(self, 'individual', self.model.mapper.table.name)
        
        if request.method == 'POST':
            # update the object with the posted data
            obj.update(**m.request_args[model_name])
            
            if obj.validate():
                #session['message'] = 'Object has been updated successfully.'
                objectstore.commit()
            else:
                #session['message'] = 'Object failed to update, errors present.'
                objectstore.clear()

        # assign to the template global
        setattr(c, model_name, obj)
        # call the template
        m.subexec('%s/edit.myt' % model_name)
    
    def delete(self, id):
        """Delete the submission type

        GET will return a form asking for approval.

        POST requests will delete the item.
        """
        # Get the object
        obj = self.model.get(id)
        if not obj:
            #session['message'] = 'No such id.'
            #session.save()
            return h.redirect_to(action='index', id=None)
        
        if request.method == 'POST':
            objectstore.delete(obj)
            objectstore.commit()
            return h.redirect_to(action='index', id=None)

        # get the model name
        model_name = getattr(self, 'individual', self.model.mapper.table.name)
        # call the template
        m.subexec('%s/confirm_delete.myt' % model_name)

class View(object):
    def _can_edit(self):
        return issubclass(self.__class__, Modify)
    
    def index(self):
        """Show a list of all objects currently in the system."""
        # GET, POST -> return list of objects

        # get name we refer to the model by in the controller
        model_name = getattr(self, 'individual', self.model.mapper.table.name)
        
        #options = getattr(self, 'conditions', {})
        #pages, collection = paginate(self.model.mapper, m.request_args.get('page', 0), **options)
        #setattr(c, model_name + '_pages', pages)
        #setattr(c, model_name + '_collection', collection)

        # assign list of objects to template global
        setattr(c, model_name + '_collection', self.model.select())
        
        c.can_edit = self._can_edit()
        # exec the template
        m.subexec('%s/list.myt' % model_name)
    
    def view(self, id):
        """View a specific object"""
        # GET, POST -> return subtype

        # get the name we're referring this object to by from the model
        model_name = getattr(self, 'individual', self.model.mapper.table.name)
        # assign to the template global
        setattr(c, model_name, self.model.get(id))
        c.can_edit = self._can_edit()
        # exec the template
        m.subexec('%s/view.myt' % model_name)
