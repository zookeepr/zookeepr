from zookeepr.lib.base import *
from zookeepr.lib.crud import Read, Update, List
from zookeepr.lib.auth import SecureController, AuthRole, AuthFunc
from zookeepr import model
from zookeepr.model.core.domain import Role
from zookeepr.model.core.tables import person_role_map
from sqlalchemy import and_

class ProfileController(SecureController, Read, Update, List):
    model = model.Person
    individual = 'profile'

    permissions = {'view': [AuthFunc('is_same_id'), AuthRole('organiser')],
                   'roles': [AuthRole('organiser')]}

    def index(self):
        r = AuthRole('organiser')
        if 'signed_in_person_id' in session:
            c.signed_in_person = self.dbsession.get(model.Person, session['signed_in_person_id'])
            if not r.authorise(self):
                redirect_to(action='view', id=session['signed_in_person_id'])
        else:
            abort(403)

        return super(ProfileController, self).index()

    def view(self):
        # hack because we don't use SecureController

        c.registration_status = request.environ['paste.config']['app_conf'].get('registration_status')
        if 'signed_in_person_id' in session:
            c.signed_in_person = self.dbsession.get(model.Person, session['signed_in_person_id'])
            roles = self.dbsession.query(Role).select()
            for role in roles:
                r = AuthRole(role.name)
                if r.authorise(self):
                    setattr(c, 'is_%s_role' % role.name, True)

        return super(ProfileController, self).view()

    def roles(self):
        """ Lists and changes the person's roles. """

        td = '<td valign="middle">'
        res = ''
        res += '<b>'+c.signed_in_person.fullname+'</b><br>'
        data = dict(request.POST)
	if data:
	  role = int(data['role'])
	  act = data['commit']
	  if act not in ['Grant', 'Revoke']: raise "foo!"
	  r = self.dbsession.query(Role).get_by(id=role)
	  res += '<p>' + act + ' ' + r.name + '.'
	  if act=='Revoke':
	    person_role_map.delete(and_(
	      person_role_map.c.person_id == self.obj.id,
	      person_role_map.c.role_id == role)).execute()
	  if act=='Grant':
	    person_role_map.insert().execute(person_id = self.obj.id,
							    role_id = role)


        res += '<table>'
        for r in self.dbsession.query(Role).select():
	  res += '<tr>'
	  # can't use AuthRole here, because it may be out of date
	  has = len(person_role_map.select(whereclause = 
	    and_(person_role_map.c.person_id == self.obj.id,
	      person_role_map.c.role_id == r.id)).execute().fetchall())

	  if has>1:
	    # this can happen if two people Grant at once, or one person
	    # does a Grant and reloads/reposts.
	    res += td + 'is %d times' % has
	    has = 1
	  else:
	    res += td+('is not', 'is')[has]
	  res += td+r.name

	  res += td+h.form(h.url())
	  res += h.hidden_field('role', r.id)
	  res += h.submit(('Grant', 'Revoke')[has])
	  res += h.end_form()

        res += '</table>'

	return Response(res)

    def is_same_id(self, *args):
        return self.obj.id == session['signed_in_person_id']
