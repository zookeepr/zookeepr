from datetime import datetime
from zookeepr.lib.base import *
from zookeepr.lib.auth import SecureController, AuthRole
from zookeepr.controllers.proposal import Proposal
from zookeepr.model import Registration, Person

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
 	  ('/discount_code', ''' Discount / group-booking codes '''),
 	  ('/profile', ''' List of all website accounts (with links...)'''),
 	  ('/invoice/remind', ''' '''),
 	  ('/openday', ''' '''),
 	  ('/proposal', ''' '''),
 	  ('/registration', ''' Summary of registrations '''),
 	  ('/invoice', ''' List of invoices (that is, registrations).'''),
 	  ('/pony', ''' OMG! Ponies!!!'''),

          ('/proposal', ''' To see what you need to reveiw '''),
          ('/review', ''' To see what you have reviewed '''),
          ('/proposal/summary', ''' summary of the reviewed papers '''),
          ('/review/summary', ''' summary of reviews '''),

          ('/registration/list_miniconf_orgs', ''' list of miniconf
	  organisers (as the registration code knows them, for miniconf
	  discount) '''),

	]

	# show it!
        c.columns = ['page', 'description']
	c.data = [('<a href="%s">%s</a>'%(fn,fn), desc)
						   for (fn, desc) in funcs]
        c.text = 'List of admin functions.'
	c.noescape = True
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
    def acc_papers_details(self):
        """ Accepted papers with bios and abstracts """
	return sql_response("""
	  SELECT proposal.id, proposal.title,
	    person.firstname || ' ' || person.lastname as name,
	    proposal.abstract, person.bio
	  FROM proposal
	    LEFT JOIN person_proposal_map
	      ON(person_proposal_map.proposal_id=proposal.id)
	    LEFT JOIN person
	      ON (person.id=person_proposal_map.person_id)
	    LEFT JOIN assistance_type
	      ON(assistance_type.id=proposal.assistance_type_id)
	  WHERE proposal.accepted=true and proposal_type_id=1
	  GROUP BY proposal.id, proposal.title, 
	    person.firstname, person.lastname, assistance_type.name,
	    proposal.abstract, person.bio
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

    def t_shirts(self):
        """ T-shirts that have been ordered and paid for """
	normal = {}; extra = []
	total_n = 0; total_e = 0
	for r in self.dbsession.query(Registration).select():
	    paid = r.person.invoices and r.person.invoices[0].paid()
	    if paid or r.person.is_speaker():
	        normal[r.teesize] = normal.get(r.teesize, 0) + 1
		total_n += 1
	    if paid and r.extra_tee_count:
	        extra.append((r.id, r.extra_tee_count, r.extra_tee_sizes,
				           r.person.email_address, r.teesize))
		total_e += int(r.extra_tee_count)
	        
        c.text = '<h2>Normal T-shirts</h2>'
	c.columns = 'M/F', 'style', 'size', 'count'
	c.data = [s.split('_') + [cnt] for (s, cnt) in normal.items()]
	c.data.sort()
        c.text = render('admin/table.myt', fragment=True)

	c.text += '<br/><h2>Extra T-shirts</h2>'
	c.text += '''(The "normal" column is for reference only; it's
				already included in the above table.)'''
	c.columns = 'rego', 'count', 'styles and sizes', 'e-mail', 'normal'
	c.data = extra
	c.data.sort()
        c.text = render('admin/table.myt', fragment=True)

	c.text += '<br/><h2>Totals</h2>'
	c.columns = ('type', 'total')
	c.data = [
	  ('Normal', total_n),
	  ('Extra', total_e),
	  ('All', total_n + total_e),
	]
	return render_response('admin/table.myt')

    def countdown(self):
        """ How many days until conference opens """
	timeleft = datetime(2008, 1, 28, 9, 0, 00) - datetime.now()
	res = Response ("%.1f days" % (timeleft.days +
					       timeleft.seconds / (3600*24.)))
	res.headers['Refresh'] = 3600
	return res

    def speakers(self):
        """ Listing of speakers and various stuff about them """
	c.data = []
	c.noescape = True
	cons_list = ('speaker_record', 'speaker_video_release',
						  'speaker_slides_release')
        speaker_list = []
	for p in self.dbsession.query(Person).select():
	    if not p.is_speaker(): continue
	    speaker_list.append((p.lastname.lower()+' '+p.firstname, p))
        speaker_list.sort()

        for (sortkey, p) in speaker_list:
	    res = [
      '%s %s (<a href="/profile/%d">%d</a>, <a href="mailto:%s">email</a>)'
		  % (p.firstname, p.lastname, p.id, p.id, p.email_address)
	    ]
	    if p.bio:
	      res.append(len(p.bio))
	    else:
	      res.append('-')
	    talks = [talk for talk in p.proposals if talk.accepted]
	    res.append('; '.join([
		'<a href="/programme/detail?TalkID=%d">%s</a>'
				% (t.id, h.truncate(t.title)) for t in talks]))
	    res.append('; '.join([t.assistance.name.replace(' assistance', '')
							      for t in talks]))
	    if p.registration:
	      if p.invoices:
		if p.invoices[0].paid():
		  res.append('OK')
		else:
		  res.append('<a href="/invoice/%d">owes $%.2f</a>'%(
			   p.invoices[0].id, p.invoices[0].total()/100.0) )
	      else:
		res.append('no invoice')

              res[-1] += ' (<a href="/registration/%d">%d</a>)' % (
				     p.registration.id, p.registration.id )

              cons = [con.replace('_', ' ') for con in cons_list
					   if getattr(p.registration, con)] 
              if len(cons)==3:
	        res.append('all')
	      elif len(cons)==0:
	        res.append('-')
	      else:
	        res.append(' and '.join(cons))

	      if p.registration.accommodation:
	        acc = p.registration.accommodation.name
		if p.registration.accommodation.option:
		  acc += ' (%s)' % p.registration.accommodation.option
		acc += ' [%d&#8211;%d]' % (p.registration.checkin,
						   p.registration.checkout)
	        res.append(acc)
	      else:
	        res.append('-')
	    else:
	      res+=['no rego', '', 'no rego']
	    #res.append(`dir(p.registration)`)
	    c.data.append(res)
	c.columns = ('name', 'bio', 'talk', 'assist',
	             'rego', 'c', 'accom')
        c.text = '''
	  Fields:
	    bio = length of bio (characters);
	    c = consent for recording/video/slides
	'''
	return render_response('admin/table.myt')
    def special_requirements(self):
        """ Special requirements and diets """
	c.data = []
        for (r_id,) in sql_data(r"""
	  select id from registration
	  where (diet ~ '.*\\S.*' or special ~ '.*\\S.*')
	  order by id
	"""):
	  r = self.dbsession.query(Registration).get(r_id)
	  p = r.person
	  if (p.invoices and p.invoices[0].paid()) or p.is_speaker():
	    if p.is_speaker():
	      speaker = 's'
	    else:
	      speaker = ''
	    c.data.append((
	      '<a href="/registration/%d">%d</a>'%(r.id, r.id),
	      '<a href="mailto:%s">%s %s'% (h.esc(p.email_address),
				    h.esc(p.firstname), h.esc(p.lastname)),
              speaker,
	      h.esc(r.dinner),
	      h.esc(r.diet),
	      h.esc(r.special)
	    ))
	c.noescape = True
	c.text = 's = speaker; ED = extra dinners'
	c.columns = ('rego', 'name / email', 's', 'ED', 'diet', 'special reqs')
	return render_response('admin/table.myt')
    def payments_received(self):
        """ Payments received, as known by zookeepr """
	return sql_response("""
	  select invoice_id, trans_id, amount, auth_num, status, result, ip_address, to_char(creation_timestamp, 'YYYY-MM-DD') as date
	  from payment_received
	  order by trans_id;
	""")
    def tentative_regos(self):
        """ People who have tentatively registered but not paid and aren't
	speakers. """
	c.data = []
	for r in self.dbsession.query(Registration).select():
	    p = r.person
	    if (p.invoices and p.invoices[0].paid()) or p.is_speaker():
	      continue
            if p.invoices:
	      amt = "$%.2f" % (p.invoices[0].total()/100.0)
	    else:
	      amt = '-'
            if r.type in ("Professional", "Hobbyist"):
	      c.data.append((r.id, p.id, `p.activated`[0], r.type, amt,
				p.email_address, p.firstname, p.lastname,))
        def lastcmp(a, b):
	  return cmp(a[-1], b[-1]) or cmp(a, b)
        c.data.sort(lastcmp)
	c.text = """ People who have tentatively registered but not paid
	and aren't speakers. <b>Professional and Hobbyist only</b> at the
	moment because those are the ones to remind about earlybird expiry.
	The "act?" column lists whether the account has been activated.
	"""
	c.columns = ('rego', 'person', 'act?', 'type', 'amount',
					  'email', 'firstname', 'lastname')
	return render_response('admin/table.myt')

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
