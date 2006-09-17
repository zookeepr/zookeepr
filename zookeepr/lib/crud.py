#from webhelpers.pagination import paginate

# FIXME: Find somewhere to document the class attributes used by the generics.

from formencode import Invalid

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
        redirect_to(**redirect_args)


class Create(CRUDBase):
    def new(self):
        """Create a new object.

        GET requests will return a blank for for submitting all attributes.

        POST requests will create the object, if the schemas validate.
        """

        model_name = self.individual
        errors = {}
        defaults = dict(request.POST)

        self.obj = self.model()
        if request.method == 'POST' and defaults:
            result, errors = self.schemas['new'].validate(defaults)

            if not errors:
                # update the new object with the form data
                for k in result[model_name]:
                    setattr(self.obj, k, result[model_name][k])

                g.objectstore.save(self.obj)
                g.objectstore.flush()

                default_redirect = dict(action='view', id=self.identifier(self.obj))
                self.redirect_to('new', default_redirect)

        # make new_object accessible to the template
        setattr(c, model_name, self.obj)

        # unmangle the errors
        good_errors = {}
        for key in errors.keys():
            try:
                for subkey in errors[key].keys():
                    good_errors[key + "." + subkey] = errors[key][subkey]
            except AttributeError:
                good_errors[key] = errors[key]

        return render_response('%s/new.myt' % model_name, defaults=defaults, errors=good_errors)


class List(CRUDBase):
    def _can_edit(self):
        return issubclass(self.__class__, Modify)
    
    def index(self):
        """Show a list of all objects currently in the system."""
        # GET, POST -> return list of objects

        # get name we refer to the model by in the controller
        model_name = self.individual
        
        #options = getattr(self, 'conditions', {})
        #pages, collection = paginate(object_mapper(self.model), m.request_args.get('page', 0), **options)
        #setattr(c, model_name + '_pages', pages)
        #setattr(c, model_name + '_collection', collection)

        # assign list of objects to template global
        setattr(c, model_name + '_collection', g.objectstore.query(self.model).select(order_by=self.model.c.id))

        c.can_edit = self._can_edit()
        # exec the template
        return render_response('%s/list.myt' % model_name)


class RUDBase(CRUDBase):
    """Retrieve the CRUD object given an ID.

    This intermediate class overrides the __before__ method to retrieve the
    CRUD object and attach it to the controller.  This carries meaning only to
    RUD methods -- Read, Update, and Delete.
    """

    def __before__(self, **kwargs):
        if hasattr(super(RUDBase, self), '__before__'):
            super(RUDBase, self).__before__(**kwargs)
        if 'id' not in kwargs.keys():
            raise RuntimeError, "id not in kwargs for %s" % (kwargs['action'],)
        
        use_oid = False # Determines if we look up on a key or the OID

        # FIXME: wtf.
        # Apparenlty this method gets called from classes that don't even inherit
        # from us... e.g. Create.  Return if id is None.
        if kwargs['id'] is None:
            #print "action is %s, we're in RUDBase.__before__, wtf, wah wah wah" % kwargs['action']
            return
        
        # If we can convert this to an integer then we look up based on the OID
        try:
            id = int(kwargs['id'])
            use_oid = True
        except ValueError:
            pass

        if use_oid:
            self.obj = g.objectstore.get(self.model, id)
        elif hasattr(self, 'key'):
            query_dict = {self.key: kwargs['id']}
            os = g.objectstore.query(self.model).select_by(**query_dict)
            if len(os) == 1:
                self.obj = os[0]

        if not hasattr(self, 'obj') or self.obj is None:
            abort(404, "No such object: cannot %s nonexistent id = %r" % (kwargs['action'],
                                                                          kwargs['id']))


class Update(RUDBase):
    def edit(self, id):
        """Allow editing of an object.

        GET requests return an 'edit' form, prefilled with the current
        data.

        POST requests update the object with the data posted.
        """

        errors = {}
        defaults = dict(request.POST)
        if defaults:
            result, errors = self.schemas['edit'].validate(defaults)

            if not errors:
                # update the object with the posted data
                for k in result[self.individual]:
                    setattr(self.obj, k, result[self.individual][k])

                g.objectstore.save(self.obj)
                g.objectstore.flush()

                redirect_to(action='view', id=self.identifier(self.obj))

        # save obj onto the magical c
        setattr(c, self.individual, self.obj)
        # call the template
        return render_response('%s/edit.myt' % self.individual, defaults=defaults, errors=errors)
        

class Delete(RUDBase):
    def delete(self):
        """Delete the proposal type

        GET will return a form asking for approval.

        POST requests will delete the item.
        """
        
        if request.method == 'POST' and self.obj is not None:
            g.objectstore.delete(self.obj)
            g.objectstore.flush()

            default_redirect = dict(action='index', id=None)
            self.redirect_to('delete', default_redirect)

        # save obj onto the magical c
        setattr(c, self.individual, self.obj)
        # call the template
        return render_response('%s/confirm_delete.myt' % self.individual)


class Read(RUDBase):
    def view(self):
        """View a specific object"""
        if hasattr(self, '_can_edit'):
            c.can_edit = self._can_edit()

        # save obj onto the magical c
        setattr(c, self.individual, self.obj)
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
