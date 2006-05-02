from pylons import Controller, m, h, c, g, session, request, params
#from webhelpers.pagination import paginate
from sqlalchemy import objectstore

class Modify(object):
    def new(self):
        model_name = getattr(self, 'individual', self.model.mapper.table.name)
        errors = {}
        new_data = self.model()

        #h.log(m.request_args)
        
        if request.method == 'POST':

            #h.log(m.request_args[model_name])
            new_data.update(**m.request_args[model_name])
            
            if new_data.validate():
                session['message'] = 'Object has been created, now editing.'
                session.save()
                objectstore.flush()
                h.redirect_to(action='edit', id=new_data.id)
            #else:
                #h.log('data not validated')

        setattr(c, model_name, new_data)
        m.subexec(getattr(self, 'template_prefix', '') + '/%s/new.myt' % model_name)
        
    def edit(self, id):
        #h.log(m.request_args)
        obj = self.model.get(id)
        if not obj:
            session['message'] = 'No such id.'
            session.save()
            h.redirect_to(action='index', id=None)
        
        model_name = getattr(self, 'individual', self.model.mapper.table.name)
        
        if request.method == 'POST':
            print m.request_args
            
            obj.update(**m.request_args[model_name])
            
            if obj.validate():
                session['message'] = 'Object has been updated successfully.'
                objectstore.commit()
            else:
                session['message'] = 'Object failed to update, errors present.'
                objectstore.clear()
        setattr(c, model_name, obj)
        m.subexec(getattr(self, 'template_prefix', '') + '/%s/edit.myt' % model_name)
    
    def delete(self, id):
        obj = self.model.get(id)
        if not obj:
            session['message'] = 'No such id.'
            session.save()
            h.redirect_to(action='index', id=None)
        
        if request.method == 'POST':
            objectstore.delete(obj)
            objectstore.commit()
            h.redirect_to(action='index')

        model_name = getattr(self, 'individual', self.model.mapper.table.name)
        m.subexec(getattr(self, 'template_prefix', '') + '/%s/confirm_delete.myt' % model_name)

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
