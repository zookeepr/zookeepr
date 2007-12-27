from datetime import datetime
import re
from zookeepr.lib.base import *
from zookeepr.lib.auth import SecureController, AuthRole
from zookeepr.controllers.proposal import Proposal
from zookeepr.model import Registration, Person, Invoice, PaymentReceived

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
			   option to view/change their zookeepr roles)
			   [auth]'''),

 	  #('/accommodation', ''' [accom] '''),
 	  ('/discount_code', ''' Discount / group-booking codes [rego] '''),
 	  ('/invoice/remind', ''' '''),
 	  ('/openday', ''' '''),
 	  ('/registration', ''' Summary of registrations, including summary
	  of accommodation [rego,accom] '''),
 	  ('/invoice', ''' List of invoices (that is, registrations). This
	  is probably the best place to check whether a given person has or
	  hasn't registered and/or paid. [rego] '''),
 	  ('/pony', ''' OMG! Ponies!!! [ZK]'''),

          ('/proposal', ''' To see what you need to reveiw [CFP] '''),
          ('/review', ''' To see what you have reviewed [CFP]'''),
          ('/proposal/summary', ''' summary of the reviewed papers [CFP] '''),
          ('/review/summary', ''' summary of reviews [CFP] '''),

          ('/registration/list_miniconf_orgs', ''' list of miniconf
	  organisers (as the registration code knows them, for miniconf
	  discount) [miniconf] '''),

	]

	# show it!
        c.columns = ['page', 'description']
	funcs = [('<a href="%s">%s</a>'%(fn,fn), desc)
						   for (fn, desc) in funcs]
	sect = {}
	pat = re.compile(r'\[([a-zA-Z,]+)\]')
        for (page, desc) in funcs:
	    m = pat.search(desc)
	    if m:
	        desc = pat.sub(r'<small>[\1]</small>', desc)
	        for s in m.group(1).split(','):
		    sect[s] = sect.get(s, []) + [(page, desc)]
	    else:
	        sect['Other'] = sect.get('Other', []) + [(page, desc)]
        c.text = '<h1>List of admin functions.</h1>'
	c.noescape = True

	sects = [(s.lower(), s) for s in sect.keys()]; sects.sort()
	c.text += ' * '.join(['<a href="#%s">%s</a>'%(s, s)
						  for s_lower, s in sects])
	for s_lower, s in sects:
	    c.text += '<br/><a name="%s"></a>' % s
	    c.text += '<h2>%s</h2>' % s
	    c.data = sect[s]
	    c.text = render('admin/table.myt', fragment=True)
	return render_response('admin/text.myt')

    def test(self):
        """
	Testing, testing, 1, 2, 3. [ZK]
        """
        return Response("This is a test. Hope you've studied!")

    def list_miniconfs(self):
        """ List of miniconfs [miniconf,CFP] """
        return sql_response("""select proposal.id as id, title, abstract,
	proposal.url, firstname || ' ' || lastname as name, email_address from proposal,
	person, person_proposal_map, account where proposal_type_id = 2 and
	person.id=person_id and person.id=account.id and proposal.id=proposal_id order by title""")
    def list_attachments(self):
        """ List of attachments [CFP] """
        return sql_response('''
	select title, filename from attachment, proposal where proposal.id=proposal_id;

	''')
    def account_creation(self):
        """ When did people create their accounts? [auth] """
	return sql_response("""select person.id, firstname || ' ' ||
	lastname as name, creation_timestamp as created from account,
	person where account.id=person.id order by person.id;
	""")
    def auth_users(self):
        """ List of users that are authorised for some role [auth] """
	return sql_response("""select role.name as role, firstname || ' '
	|| lastname as name, email_address, person.id
	from role, person, person_role_map, account
	where person.id=person_id and role.id=role_id and account.id=account_id
	order by role, lastname, firstname""")
    def rej_papers(self):
        """ Rejected papers, without abstracts (for the miniconf
	organisers) [CFP,miniconf] """
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
        """ Rejected papers, with abstracts (for the miniconf organisers)
	[CFP] """
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
        """ Accepted papers (for miniconf organisers)
	[CFP,miniconf,speaker]"""
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
        """ Accepted papers with bios and abstracts [CFP] """
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
        """ Accepted papers/tutes with type and travel assistance status
	[CFP,speaker]"""
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
        """ All registrations with everything [rego]"""
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
        """ T-shirts that have been ordered and paid for [rego] """
	normal = {}; organiser = {}; extra = []
	total_n = 0; total_o = 0; total_e = 0
	for r in self.dbsession.query(Registration).select():
	    paid = r.person.invoices and r.person.invoices[0].paid()
	    if paid or r.person.is_speaker():
	        if r.type in ("Monday pass", "Tuesday pass"):
		    pass # sorry, had to say it :-)
		else:
		    normal[r.teesize] = normal.get(r.teesize, 0) + 1
		    total_n += 1
		if 'organiser' in [rl.name for rl in r.person.roles]:
		    organiser[r.teesize] = organiser.get(r.teesize, 0) + 1
		    total_o += 1
	    if paid and r.extra_tee_count:
	        extra.append((r.id, r.extra_tee_count, r.extra_tee_sizes,
				           r.person.email_address, r.teesize))
		total_e += int(r.extra_tee_count)
	        
        c.text = '<h2>Normal T-shirts</h2>'
	c.text += '''(Includes organisers. So we can blend.)'''
	c.columns = 'M/F', 'style', 'size', 'count'
	c.data = [s.split('_') + [cnt] for (s, cnt) in normal.items()]
	c.data.sort()
        c.text = render('admin/table.myt', fragment=True)

        c.text += '<h2>Organiser T-shirts</h2>'
	c.text += '''(Based on the 'organiser' role in zookeepr.)'''
	c.columns = 'M/F', 'style', 'size', 'count'
	c.data = [s.split('_') + [cnt] for (s, cnt) in organiser.items()]
	c.data.sort()
        c.text = render('admin/table.myt', fragment=True)

	c.text += '<br/><h2>Extra T-shirts</h2>'
	c.text += '''(The "normal" column is for reference only; it's
			     already included in the first table above.)'''
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
	  ('Organiser', total_o),
	]
	return render_response('admin/table.myt')

    def t_shirts_F_long_18(self):
        """ T-shirts that have been ordered and paid for in size F_long_18
	[rego] """
	c.data = []
	for r in self.dbsession.query(Registration).select():
	    paid = r.person.invoices and r.person.invoices[0].paid()
	    if paid or r.person.is_speaker():
	        if r.type in ("Monday pass", "Tuesday pass"):
		    pass # sorry, had to say it :-)
		elif r.teesize == 'F_long_18':
		    c.data += [[r.teesize, r.person.firstname,
				r.person.lastname, r.person.email_address]]
		    if 'organiser' in [rl.name for rl in r.person.roles]:
			c.data[-1] += ['organiser']
	        
        c.text = """<h2>F_long_18 T-shirts</h2> Note: <b>does not include
	extra</b> t-shirts."""
	c.data.sort()
	return render_response('admin/table.myt')

    def countdown(self):
        """ How many days until conference opens """
	timeleft = datetime(2008, 1, 28, 9, 0, 00) - datetime.now()
	res = Response ("%.1f days" % (timeleft.days +
					       timeleft.seconds / (3600*24.)))
	res.headers['Refresh'] = 3600
	return res

    def speakers(self):
        """ Listing of speakers and various stuff about them [speaker] """
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

	# sort by rego status (while that's important)
	def my_cmp(a,b):
	    return cmp(a[4], b[4])
	c.data.sort(my_cmp)

	c.columns = ('name', 'bio', 'talk', 'assist',
	             'rego', 'c', 'accom')
        c.text = '''
	  Fields:
	    bio = length of bio (characters);
	    c = consent for recording/video/slides
	'''
	return render_response('admin/table.myt')
    def special_requirements(self):
        """ Special requirements and diets [rego] """
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
	      r.type,
              speaker,
	      h.esc(r.dinner),
	      h.esc(r.diet),
	      h.esc(r.special)
	    ))
	c.noescape = True
	c.text = 's = speaker; ED = extra dinners'
	c.columns = ('rego', 'name / email', 'rego type', 's', 'ED', 'diet', 'special reqs')
	return render_response('admin/table.myt')
    def payments_received(self):
        """ Payments received, as known by zookeepr [rego] """
	return sql_response("""
	  select invoice_id, trans_id, amount, auth_num, status, result, ip_address, to_char(creation_timestamp, 'YYYY-MM-DD') as date
	  from payment_received
	  order by trans_id;
	""")

    def tentative_regos(self):
        """ People who have tentatively registered but not paid and aren't
	speakers. [rego] """
	c.data = []
	for r in self.dbsession.query(Registration).select():
	    p = r.person
	    if (p.invoices and p.invoices[0].paid()) or p.is_speaker():
	      continue
            if p.invoices:
	      amt = "$%.2f" % (p.invoices[0].total()/100.0)
	    else:
	      amt = '-'
	    if r.discount_code:
	      if r.discount:
		dc = r.discount.percentage
              else:
	        dc = 'invalid'
	    else:
	      dc = '-'
            if True or r.type in ("Professional", "Hobbyist"):
	      c.data.append((r.id, p.id, `p.activated`[0], r.type, dc, amt,
				p.email_address, p.firstname, p.lastname,))
        def lastcmp(a, b):
	  return cmp(a[-1], b[-1]) or cmp(a, b)
        c.data.sort(lastcmp)
	c.text = """ People who have tentatively registered but not paid
	and aren't speakers. """
	# <b>Professional and Hobbyist only</b> at the
	# moment because those are the ones to remind about earlybird expiry.
	c.text += """ The "act?" column lists whether the account has been
	activated; dc=discount code (percentage).  """
	c.columns = ('rego', 'person', 'act?', 'type', 'dc', 'amount',
					  'email', 'firstname', 'lastname')
	return render_response('admin/table.myt')

    def newcomers(self):
        """ People who have not ticked any of the "previously attended"
	boxes. [rego] """
	c.text = """ People who have not ticked any of the "previously
	attended" boxes. """
	c.data = []
	for r in self.dbsession.query(Registration).select():
	    if r.prevlca:
	        continue
	    p = r.person
	    if p.is_speaker():
	        if r.type != 'Speaker':
		    comment = ' (speaker)'
		else:
		    comment = ''
	    elif p.invoices and p.invoices[0].paid():
	        comment = ''
	    else:
	        continue
            c.data.append((p.lastname.lower(), p.firstname.lower(), p.id,
							    r, p, comment))
        c.data.sort()
	c.data = [(p.id, r.id, p.firstname + ' ' + p.lastname, p.email_address,
							   r.type + comment)
	    for (last, first, id, r, p, comment) in c.data]
        c.columns = ('person', 'rego', 'name', 'email', 'type')
	return render_response('admin/table.myt')
    def partners_programme(self):
        """ Partners programme information [PP] """

	fields = ('pp_adults', 'kids_12_17', 'kids_10_11', 'kids_7_9',
						    'kids_4_6', 'kids_0_3')

	c.text = """ Data for the partners programme. Note that the partner
	e-mail address is not validated in any way, unlike the rego e-mail.
	The last row is totals. The last column contains the "diet" and
	"special requirements" from the rego, in case they refer to the
	partner (there aren't separate ones for PP). """

	c.data = []
	totals = dict([(f, 0) for f in fields])
	for r in self.dbsession.query(Registration).select():
	    comments = []
	    if not r.partner_email:
	        continue
	    p = r.person
	    if p.is_speaker():
		comments += ['speaker partner']
	    elif p.invoices and p.invoices[0].paid():
	        pass
	    else:
	        continue
            row = [r.partner_email] 
	    row += [getattr(r, f) for f in fields]
	    for f in fields:
	        if getattr(r, f):
		    totals[f] += getattr(r, f)
	    if r.diet:
	        comments += ['rego diet: ' + r.diet]
	    if r.special:
	        comments += ['rego special: ' + r.special]
	    row += [p.email_address, '; '.join(comments)]
            c.data.append(row)

        row = [u'\u2211: %s' % sum(totals.values())]
	row += [totals[f] for f in fields]
	c.data.append(row)

	c.columns = ['email'] 
	c.columns += [re.sub('^.*?_', '', f).replace('_', '-') for f in fields]
	c.columns += ['rego email', 'comment'] 
	return render_response('admin/table.myt')

    def accom_summary(self):
        """ Summary of accommodation. [accom] """
	def blank_accom():
	  blank = {}
	  for d in (27,28,29,30,31,1,2,3):
	    blank[d] = {'ci': 0, 'co': 0}
	  return blank

	c.data = []
	d = {}
	for r in self.dbsession.query(Registration).select():
	    p = r.person
	    if not ((p.invoices and p.invoices[0].paid()) or p.is_speaker()):
	      continue
	    if not r.accommodation: continue
	    if not d.has_key(r.accommodation.name):
	      d[r.accommodation.name] = blank_accom()
	    if not d[r.accommodation.name].has_key(r.checkin):
	      d[r.accommodation.name][r.checkin] = {'ci': 0, 'co': 0}
	    if not d[r.accommodation.name].has_key(r.checkout):
	      d[r.accommodation.name][r.checkout] = {'ci': 0, 'co': 0}
	    d[r.accommodation.name][r.checkin]['ci'] += 1
	    d[r.accommodation.name][r.checkout]['co'] += 1

	def date_sort(a, b):
	  if a<15: a+=100
	  if b<15: b+=100
	  return cmp(a, b)

        cum = 0
	for name in d.keys():
	  dates = d[name].keys()
	  dates.sort(date_sort)
	  for date in dates:
	    ci = d[name][date]['ci']; co = d[name][date]['co']
	    cum += ci - co
	    c.data.append((name, date, ci, co, cum))
	  if cum != 0:
	    c.data.append(('error! in/out mismatch!', '', '', cum, 0))
	    cum = 0

        c.text = """ Summary of accommodation. Summarises how many people
	are checking in and out of each accommodation, and therefore how
	many will be sleeping there that night. Note: skips days outside
	the conf on which there is no change. """
        c.columns = 'where', 'day', 'in', 'out', 'beds'
	return render_response('admin/table.myt')

    def accom_details(self):
        """ List of accommodation. [accom] """
	c.data = []
	d = {}
	for r in self.dbsession.query(Registration).select():
	    p = r.person
	    if not ((p.invoices and p.invoices[0].paid()) or p.is_speaker()):
	      continue
	    if not r.accommodation: continue
	    comments = []
	    if r.diet: comments.append('diet: '+r.diet)
	    if r.special: comments.append('special: '+r.special)
	    comments = '; '.join(comments)
	    c.data.append((r.accommodation.name, p.firstname, p.lastname,
		p.email_address, p.phone, r.checkin, r.checkout, comments))

	def my_cmp(a, b):
	  if cmp(a[0], b[0]):
	      return cmp(a[0], b[0])
	  a_day = a[5]
	  b_day = b[5]
	  if a_day<15: a_day+=100
	  if b_day<15: b_day+=100
	  if cmp(a_day, b_day):
	      return cmp(a_day, b_day)
	  if cmp(a[2].lower(), b[2].lower()):
	      return cmp(a[2].lower(), b[2].lower())
	  return cmp(a, b)

	c.data.sort(my_cmp)

	c.text = """ List of accommodation. Sorted by location, checkin,
	lastname. For totals, see the summary instead. """

        c.columns = ('where', 'first', 'last', 'email', 'phone', 'in',
							  'out', 'comment')
	return render_response('admin/table.myt')

    def acc_papers_xml(self):
        """ An XML file with titles and speakers of accepted talks, for use
	in AV splash screens [CFP,AV] """
	c.talks = self.dbsession.query(Proposal).select_by(accepted=True)

	res = render_response('admin/acc_papers_xml.myt', fragment=True)
	res.headers['Content-type']='text/plain; charset=utf-8'
	return res
    def paid_summary(self):
        """ Summary of paid invoices. [rego] """
	def add(key, amt, qty):
	    if amt==0: return
	    amt /= 100.0
	    if total.has_key(key):
	        total[key][0] += qty
	        total[key][1] += amt
	    else:
	        total[key] = [qty, amt]

        keywords = ('Registration', 'Accommodation', 'Discount', 'Partner',
							       'earlybird')

	total = {}
	add(u'\u2211', 1120, 1)
	add(u'[test payments]', 1120, 1)

	for i in self.dbsession.query(Invoice).select():
	    if not i.paid():
	        continue
            for ii in i.items:
		desc = ii.description
	        amt = ii.total()
		add(desc, amt, ii.qty)
		add(u'\u2211', amt, ii.qty)
		for kw in keywords:
		    if kw in desc:
			add(u'\u2211 '+kw, amt, ii.qty)
        c.columns = 'description', 'count', 'Inc GST', 'Ex GST', 'GST'
        c.data = [(desc, qty, h.number_to_currency(amt),
	           h.number_to_currency(amt * 10/11.),
	           h.number_to_currency(amt / 11.))
				   for (desc, (qty, amt)) in total.items()]
	c.data.sort()
	c.text = "Summary of paid invoices."
	return render_response('admin/table.myt')

    def miniconf_interest(self):
	""" What people ticked for the "interested in miniconf" question.
	[miniconf] """
	count={}; lencount={}; total=0
	for r in paid_regos(self):
	    if r.miniconf:
	        for mc in r.miniconf:
		    count[mc] = count.get(mc, 0) + 1
		length = len(r.miniconf)
	    else:
	        length = 0
	    lencount[length] = lencount.get(length, 0) + 1
	    total += 1

        c.text = "Which ones people selected."
        c.data = []
        for mc in count.keys():
	    c.data += [(mc, count[mc], "%.1f%%"%(count[mc]*100.0/total))]
        c.data.sort()
	c.text = render('admin/table.myt', fragment=True)

        c.text += "How many people selected."
        c.data = []
        for l in lencount.keys():
	    c.data += [(l, lencount[l], "%.1f%%"%(lencount[l]*100.0/total))]
        c.data.sort()
	return render_response('admin/table.myt')
    def discount_code_details(self):
        """ Have discount code users paid their accom and other extras?
	[rego] """
        c.data = []
	for r in self.dbsession.query(Registration).select():
	    if not r.discount_code:
	        continue
	    p = r.person
	    row = ['<a href="/registration/%d">%d</a>'%(r.id, r.id), p.id,
			      p.firstname + ' ' + p.lastname, r.discount_code]
	    if r.discount:
	      row.append(r.discount.percentage)
	    else:
	      row.append('invalid')
	    if p.invoices:
	      if p.invoices[0].paid():
		row.append('<a href="/invoice/%d">OK</a>'%p.invoices[0].id)
	      else:
		row.append('<a href="/invoice/%d">owes $%.2f</a>'%(
			 p.invoices[0].id, p.invoices[0].total()/100.0) )
	    else:
	      row.append('no invoice')
	    c.data.append(row)

        c.header = 'rego', 'person', 'name', 'code', '%', 'paid'
	c.noescape = True
	return render_response('admin/table.myt')
    def reconcile(self):
        """ Reconcilliation between D1 and ZK; for now, compare the D1 data
	that have been placed in the fixed location in the filesystem and
	work from there... [rego] """
        import csv
	d1_data = csv.reader(file('/home/jiri/mel8/reconcile-20071227/linux_report_27122007.csv'))
	d1_cols = d1_data.next()
	d1_cols = [s.strip() for s in d1_cols]

	all = {}

	t_offs = d1_cols.index('payment_id')
	amt_offs = d1_cols.index('payment_amount')
	d1 = {}
	for row in d1_data:
	  t = row[t_offs]
	  amt = row[amt_offs]
	  if amt[-3]=='.':
	    # remove the decimal point
	    amt = amt[:-3] + amt[-2:]
	  row.append(amt)
	  all[t] = 1
	  if d1.has_key(t):
	    d1[t].append(row)
	  else:
	    d1[t] = [row]

	zk = {}
	for p in self.dbsession.query(PaymentReceived).select():
	  t = p.TransID
	  all[t] = 1
	  if zk.has_key(t):
	    zk[t].append(p)
	  else:
	    zk[t] = [p]
	  
	zk_fields =  ('InvoiceID', 'TransID', 'Amount', 'AuthNum',
				'Status', 'result', 'HTTP_X_FORWARDED_FOR')

        all = all.keys()
	all.sort()
	c.data = []
	for t in all:
	  zk_t = zk.get(t, []); d1_t = d1.get(t, [])
	  if len(zk_t)==1 and len(d1_t)==1:
	    if str(zk_t[0].Amount) == d1_t[0][-1]:
	      continue
	  c.data.append((
	    '; '.join([', '.join([str(getattr(z, f)) for f in zk_fields])
           						   for z in zk_t]),
	    t,
	    '; '.join([', '.join(d) for d in d1_t])
	  ))

	return render_response('admin/table.myt')

        

def paid_regos(self):
    for r in self.dbsession.query(Registration).select():
	p = r.person
	if (p.invoices and p.invoices[0].paid()) or p.is_speaker():
	    yield r

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
