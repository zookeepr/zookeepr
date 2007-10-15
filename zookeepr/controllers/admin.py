from zookeepr.lib.base import *
from zookeepr.lib.auth import SecureController, AuthRole
from zookeepr.controllers.proposal import Proposal

class AdminController(SecureController):
    """ Miscellaneous admin tasks. """

    permissions = {
      'ALL': [AuthRole('organiser')],
      'acc_papers': [AuthRole('miniconf'), AuthRole('organiser')],
      'rej_papers': [AuthRole('miniconf'), AuthRole('organiser')],
      'rej_papers_abstracts': [AuthRole('miniconf'), AuthRole('organiser')],
    }
    def index(self):
        res = dir(self)
	exceptions = ['check_permissions', 'dbsession', 'index',
			      'logged_in', 'permissions', 'start_response']

	# get the ones in this controller by introspection.
	funcs = [('/admin/'+x, getattr(self, x).__doc__)
		       for x in res if x[0] != '_' and x not in exceptions]

        # other functions should be appended to the list here.
	funcs += [
	  ('/profile', '''List of people signed up to the webpage (with
			   option to view/change their zookeepr roles)'''),

 	  ('/accommodation', ''' '''),
 	  ('/discount_code', ''' '''),
 	  ('/profile', ''' List of all website accounts (with links...)'''),
 	  ('/invoice/remind', ''' '''),
 	  ('/openday', ''' '''),
 	  ('/proposal', ''' '''),
 	  ('/registration', ''' '''),
 	  ('/pony', ''' OMG! Ponies!!!'''),

          ('/proposal', ''' To see what you need to reveiw '''),
          ('/review', ''' To see what you have reviewed '''),
          ('/proposal/summary', ''' summary of the reviewed papers '''),
          ('/review/summary', ''' summary of reviews '''),

	]

	# show it!
        c.columns = ['page', 'description']
	c.data = [('<a href="%s">%s</a>'%(fn,fn), desc)
						   for (fn, desc) in funcs]
        c.text = 'List of admin functions.'
	return render_response('admin/table.myt')

    def test(self):
        """
	Testing, testing, 1, 2, 3.
        """
        return Response("This is a test. Hope you've studied!")

    def list_miniconfs(self):
        """ List of miniconfs """
        return sql_response("""select proposal.id as id, title, abstract,
	proposal.url, firstname || ' ' || lastname as name, email_address from proposal,
	person, person_proposal_map, account where proposal_type_id = 2 and
	person.id=person_id and person.id=account.id and proposal.id=proposal_id order by title""")
    def list_attachments(self):
        """ List of attachments """
        return sql_response('''
	select title, filename from attachment, proposal where proposal.id=proposal_id;

	''')
    def account_creation(self):
        """ When did people create their accounts? """
	return sql_response("""select person.id, firstname || ' ' ||
	lastname as name, creation_timestamp as created from account,
	person where account.id=person.id order by person.id;
	""")
    def auth_users(self):
        """ List of users that are authorised for some role """
	return sql_response("""select role.name as role, firstname || ' '
	|| lastname as name, person.id from role, person, person_role_map
	where person.id=person_id and role.id=role_id order by role,
	lastname, firstname""")
    def rej_papers(self):
        """ Rejected papers, without abstracts (for the miniconf organisers) """
	return sql_response("""
	  select distinct miniconf, proposal.id as p,
	    firstname || ' ' || lastname as name,
	    title, project,
	    proposal.url, email_address as email, person.url as homepage
	  from proposal, person, account, person_proposal_map, review
	  where person_id = person.id and review.proposal_id = proposal.id
	    and person_proposal_map.proposal_id = proposal.id
	    and account_id = account.id and account_id = person.id 
	    and proposal_type_id = 1 and accepted is null
	  order by miniconf, proposal.id
	""")
    def rej_papers_abstracts(self):
        """ Rejected papers, with abstracts (for the miniconf organisers) """
	return sql_response("""
	  select distinct miniconf, proposal.id as p,
	    firstname || ' ' || lastname as name,
	    title, project,
	    abstract,
	    proposal.url, email_address as email, person.url as homepage
	  from proposal, person, account, person_proposal_map, review
	  where person_id = person.id and review.proposal_id = proposal.id
	    and person_proposal_map.proposal_id = proposal.id
	    and account_id = account.id and account_id = person.id 
	    and proposal_type_id = 1 and accepted is null
	  order by miniconf, proposal.id
	""")
    def acc_papers(self):
        """ Accepted papers (for miniconf organisers) """
	return sql_response("""
	  SELECT proposal.id, proposal.title,
	    person.firstname || ' ' || person.lastname as name
	  FROM proposal
	    LEFT JOIN person_proposal_map
	      ON(person_proposal_map.proposal_id=proposal.id)
	    LEFT JOIN person
	      ON (person.id=person_proposal_map.person_id)
	    LEFT JOIN assistance_type
	      ON(assistance_type.id=proposal.assistance_type_id)
	  WHERE proposal.accepted=true and proposal_type_id=1
	  GROUP BY proposal.id, proposal.title, 
	    person.firstname, person.lastname, assistance_type.name
	  ORDER BY proposal.id ASC;
	""")
    def acc_papers_tutes(self):
        """ Accepted papers/tutes with type and travel assistance status """
	return sql_response("""
	  SELECT proposal.id, proposal.title,
	    person.firstname || ' ' || person.lastname as name,
	    assistance_type.name as assistance, proposal_type.name as type
	  FROM proposal
	    LEFT JOIN proposal_type
	      ON(proposal.proposal_type_id=proposal_type.id)
	    LEFT JOIN person_proposal_map
	      ON(person_proposal_map.proposal_id=proposal.id)
	    LEFT JOIN person
	      ON (person.id=person_proposal_map.person_id)
	    LEFT JOIN assistance_type
	      ON(assistance_type.id=proposal.assistance_type_id)
	  WHERE proposal.accepted=true
	  GROUP BY proposal.id, proposal.title, proposal_type.name,
	    person.firstname, person.lastname, assistance_type.name
	  ORDER BY proposal.id ASC;
	""")
    def rego_great_big_dump(self):
        """ All registrations with everything """
	return sql_response("""
	  select * from registration full outer join person on
	  person_id=person.id full outer join account on account_id=account.id
	  full outer join invoice on person.id=invoice.person_id full outer join
	  payment_received on invoice.id = payment_received.invoice_id;
	""")

    def draft_timetable(self):
        """ Draft schedule for the conference """
        def talk(id):
	    proposal = self.dbsession.query(Proposal).get(id)
	    if proposal==None:
	      return '[%s]'%id
	    res = proposal.title
	    if len(proposal.people)>0:
	        res += ' &#8212; ' + ', '.join([auth.firstname + ' ' + auth.lastname for auth in proposal.people])
	    return res
        c.talk = talk
	return render_response('admin/draft_timetable.myt')

def sql_response(sql):
    """ This function bypasses all the MVC stuff and just puts up a table
    of results from the given SQL statement.

    Ideally, of course, it should never be used.

    Example:
	def foo(self):
	    return sql_response('select * from person')
    """
    import zookeepr.model
    res = zookeepr.model.metadata.get_engine().execute(sql);
    c.columns = res.keys
    c.data = res.fetchall()
    c.sql = sql
    return render_response('admin/sqltable.myt')
    
def sql_data(sql):
    """ This function bypasses all the MVC stuff and just gives you a
    two-dimensional array based on the given SQL statement.

    Ideally, of course, it should never be used.
    """
    import zookeepr.model
    return zookeepr.model.metadata.get_engine().execute(sql).fetchall();
