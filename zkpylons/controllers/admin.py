import logging

from pylons import request, response, session, tmpl_context as c, app_globals
from zkpylons.lib.helpers import redirect_to
from pylons.decorators import validate
from pylons.decorators.rest import dispatch_on
import zkpylons.lib.helpers as h

from formencode import validators, htmlfill
from formencode.variabledecode import NestedVariables

from zkpylons.lib.base import BaseController, render
from zkpylons.lib.validators import BaseSchema

from authkit.authorize.pylons_adaptors import authorize
from authkit.permissions import ValidAuthKitUser

from zkpylons.model import meta, Person, Product, Registration, ProductCategory
from zkpylons.model import Proposal, ProposalType, ProposalStatus, Invoice, Funding
from zkpylons.model import Event, Schedule, TimeSlot, Location
from zkpylons.model import Fulfilment, FulfilmentItem, FulfilmentType, FulfilmentStatus, FulfilmentGroup
from zkpylons.model.funding_review import FundingReview
from zkpylons.model.payment_received import PaymentReceived
from zkpylons.model.invoice_item import InvoiceItem
from zkpylons.model.rego_note import RegoNote
from zkpylons.model.social_network import SocialNetwork
from zkpylons.model.special_registration import SpecialRegistration
from zkpylons.model.volunteer import Volunteer

from zkpylons.config.lca_info import lca_info, lca_rego

from zkpylons.lib.ssl_requirement import enforce_ssl

from sqlalchemy import and_, or_, func

log = logging.getLogger(__name__)

import re
import types

from datetime import datetime
import os, random, re, urllib

now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

class AdminController(BaseController):
    """ Miscellaneous admin tasks. """

    @enforce_ssl(required_all=True)
    def __before__(self, **kwargs):
        c.signed_in_person = h.signed_in_person()

    @authorize(h.auth.has_organiser_role)
    def index(self):
        res = dir(self)
        exceptions = ['check_permissions', 'dbsession',
                     'index', 'logged_in', 'permissions', 'start_response']

        # get the ones in this controller by introspection.
        funcs = [('/admin/'+x, getattr(self, x).__doc__ or '')
                       for x in res if x[0] != '_' and x not in exceptions]

        # other functions should be appended to the list here.
        funcs += [
          ('/db_content', '''Edit HTML pages that are stored in the database. [Content]'''),
          ('/db_content/list_files', '''List and upload files for use on the site. [Content]'''),
          ('/person', '''List of people signed up to the webpage (with option to view/change their zkpylons roles) [Accounts]'''),
          ('/social_network', '''List social networks that people can indicate they are members of [Accounts]'''),
          ('/product', '''Manage all of zkpylonss products. [Inventory]'''),
          ('/product_category', '''Manage all of zkpylonss product categories. [Inventory]'''),
          ('/voucher', '''Manage vouchers to give to delegates. [Inventory]'''),
          ('/ceiling', '''Manage ceilings and available inventory. [Inventory]'''),
          ('/registration', '''View registrations and delegate details. [Registrations]'''),
          ('/invoice', '''View assigned invoices and their status. [Invoicing]'''),
          ('/invoice/new', '''Create manual invoice for a person. [Invoicing]'''),
          ('/volunteer', '''View and approve/deny applications for volunteers. [Registrations]'''),
          ('/rego_note', '''Create and manage private notes on individual registrations. [Registrations]'''),
          ('/role', '''Add, delete and modify available roles. View the person list to actually assign roles. [Accounts]'''),
          ('/registration/generate_badges', '''Generate one or many Badges. [Registrations]'''),

          #('/accommodation', ''' [accom] '''),
          #('/voucher_code', ''' Voucher codes [rego] '''),
          ('/invoice/remind', ''' Payment reminders [Invoicing] '''),
          #('/registration', ''' Summary of registrations, including summary of accommodation [rego,accom] '''),
          #('/invoice', ''' List of invoices (that is, registrations). This is probably the best place to check whether a given person has or hasn't registered and/or paid. [rego] '''),
          #('/pony', ''' OMG! Ponies!!! [ZK]'''),

          ('/review/help', ''' Information on how to get started reviewing [CFP] '''),
          ('/proposal/review_index', ''' To see what you need to reveiw [CFP] '''),
          ('/review', ''' To see what you have reviewed [CFP]'''),
          ('/proposal/summary', ''' Summary of the reviewed proposals [CFP] '''),
          ('/review/summary', ''' List of reviewers and scores [CFP] '''),
          ('/proposal/approve', ''' Change proposal status for proposals [CFP] '''),
          ('/funding/review_index', ''' To see what you need to reveiw [Funding] '''),
          ('/funding_type', ''' Manage Funding Types [Funding] '''),
          ('/funding/approve', ''' Change proposal status for funding applications [Funding] '''),
          ('/proposal/latex', ''' Proposals with LaTeX formatting [Booklet] '''),
          ('/registration/professionals_latex', ''' Profressionals with LaTeX formatting [Booklet] '''),

          #('/registration/list_miniconf_orgs', ''' list of miniconf
          #organisers (as the registration code knows them, for miniconf
          #voucher) [miniconf] '''),

        ]

        # show it!
        c.columns = ['page', 'description']
        funcs = [('<a href="%s">%s</a>'%(fn,fn), desc)
                                                   for (fn, desc) in funcs]
        sect = {}
        pat = re.compile(r'\[([\ a-zA-Z,]+)\]')
        for (page, desc) in funcs:
            m = pat.search(desc)
            if m:
                desc = pat.sub(r'<small>[\1]</small>', desc)
                for s in m.group(1).split(','):
                    sect[s] = sect.get(s, []) + [(page, desc)]
            else:
                sect['Other'] = sect.get('Other', []) + [(page, desc)]
        c.noescape = True

        sects = [(s.lower(), s) for s in sect.keys()]; sects.sort()
        c.sects = sects
        text = ''
        sect_text = ""
        for s_lower, s in sects:
            c.text = '<a name="%s"></a>' % s
            c.text += '<h2>%s</h2>' % s
            c.data = sect[s]
            sect_text += render('admin/table_fragment.mako')

        c.text = text
        c.sect_text = sect_text
        return render('admin/text.mako')

    @authorize(h.auth.has_organiser_role)
    def rej_proposals_abstracts(self):
        """ Rejected proposals, with abstracts (for the miniconf organisers) [Schedule] """
        return sql_response("""
            SELECT
                proposal.id,
                proposal.title,
                proposal_type.name AS "proposal type",
                proposal.project,
                proposal.url as project_url,
                proposal.abstract,
                person.firstname || ' ' || person.lastname as name,
                person.email_address,
                person.url as homepage,
                person.bio,
                person.experience,
                (SELECT review2.miniconf FROM review review2 WHERE review2.proposal_id = proposal.id GROUP BY review2.miniconf ORDER BY count(review2.miniconf) DESC LIMIT 1) AS miniconf,
                MAX(review.score) as max,
                MIN(review.score) as min,
                ROUND(AVG(review.score),2) as avg
            FROM proposal
                LEFT JOIN review ON (proposal.id=review.proposal_id)
                LEFT JOIN proposal_type ON (proposal.proposal_type_id=proposal_type.id)
                LEFT JOIN stream ON (review.stream_id=stream.id)
                LEFT JOIN person_proposal_map ON (proposal.id = person_proposal_map.proposal_id)
                LEFT JOIN person ON (person_proposal_map.person_id = person.id)
                LEFT JOIN proposal_status ON (proposal.status_id = proposal_status.id)
            WHERE
                proposal_type.name <> 'Miniconf'
                AND proposal_status.name = 'Rejected'
            GROUP BY proposal.id, proposal.title, proposal_type.name, stream.name, person.firstname, person.lastname, person.email_address, person.url, person.bio, person.experience, proposal.abstract, proposal.project, proposal.url
            ORDER BY miniconf, proposal_type.name ASC
        """)

    def _collect_garbage(self):
        """
        Invoke the garbage collector. [ZK]
        """
        import gc
        before = len(gc.get_objects())
        garbage = gc.collect()
        after = len(gc.get_objects())
        uncollectable = len(gc.garbage)
        del(gc.garbage[:])
        return Response("""
        Is automatic garbage collection enabled? %s.
        <br>Garbage collector knows of %d objects.
        <br>Full collection: %d pieces of garbage found, %d uncollectable.
        <br>Garbage collector knows of %d objects.
        """ % (
          gc.isenabled(),
          before,
          garbage, uncollectable,
          after,
        ))

    @authorize(h.auth.has_organiser_role)
    def _known_objects(self):
        """
        List known objects by type. (Invokes GC first.) [ZK]
        """
        import gc
        gc.collect()
        count = {}
        objects = gc.get_objects()
        for o in objects:
          t = type(o)
          count[t] = count.get(t, 0) + 1
        total = len(objects); scale = 100.0 / total
        objects = None #avoid having the data twice...
        c.data = [(num, '%.1f%%' % (num * scale), t)
                                         for (t, num) in count.iteritems()]
        c.data.sort(reverse=True)
        c.columns = 'count', '%', 'type'
        c.text = "Total: %d" % total
        return table_response()

    @authorize(h.auth.has_organiser_role)
    def list_attachments(self):
        """ List of attachments [CFP] """
        return sql_response('''
        select title, filename from attachment, proposal where proposal.id=proposal_id;

        ''')


    @authorize(h.auth.has_organiser_role)
    def auth_users(self):
        """ List of users that are authorised for some role [Accounts] """
        return sql_response("""select role.name as role, firstname || ' '
        || lastname as name, email_address, person.id
        from role, person, person_role_map
        where person.id=person_id and role.id=role_id
        order by role, lastname, firstname""")

    @authorize(h.auth.has_organiser_role)
    def proposal_list(self):
        """ Large table of all the proposal proposals. [CFP] """
        return sql_response("""
          SELECT proposal.id, proposal.title, proposal.creation_timestamp AS ctime, proposal.last_modification_timestamp AS mtime, proposal_status.name AS status,
            person.firstname || ' ' || person.lastname as name, person.email_address
          FROM proposal, person, person_proposal_map, proposal_type, proposal_status
          WHERE proposal.id = person_proposal_map.proposal_id AND person.id = person_proposal_map.person_id AND proposal_type.id = proposal.proposal_type_id AND proposal_type.name <> 'Miniconf' AND proposal_status.id = proposal.status_id
          ORDER BY proposal.id ASC;
        """)

    @authorize(h.auth.has_organiser_role)
    def miniconf_list(self):
        """ Large table of all the miniconf proposals. [CFP] """
        return sql_response("""
          SELECT proposal.id, proposal.title, proposal.creation_timestamp AS ctime, proposal.last_modification_timestamp AS mtime, proposal_status.name AS status,
            person.firstname || ' ' || person.lastname as name, person.email_address
          FROM proposal, person, person_proposal_map, proposal_type, proposal_status
          WHERE proposal.id = person_proposal_map.proposal_id AND person.id = person_proposal_map.person_id AND proposal_type.id = proposal.proposal_type_id AND proposal_type.name = 'Miniconf' AND proposal_status.id = proposal.status_id
          ORDER BY proposal.id ASC;
        """)

    @authorize(h.auth.has_reviewer_role)
    def proposals_by_strong_rank(self):
        """ List of proposals ordered by number of certain score / total number of reviewers [CFP] """
        query = """
                SELECT
                    proposal.id,
                    proposal.title,
                    proposal_type.name AS "proposal type",
                    review.score,
                    COUNT(review.id) AS "#reviewers at this score",
                    (
                        SELECT COUNT(review2.id)
                            FROM review as review2
                            WHERE review2.proposal_id = proposal.id
                    ) AS "#total reviewers",
                    CAST(
                        CAST(
                            COUNT(review.id) AS float(8)
                        ) / CAST(
                            (SELECT COUNT(review2.id)
                                FROM review as review2
                                WHERE review2.proposal_id = proposal.id
                            ) AS float(8)
                        ) AS numeric(8,2)
                    ) AS "#reviewers at this score / #total reviews %%"
                FROM proposal
                    LEFT JOIN review ON (proposal.id=review.proposal_id)
                    LEFT JOIN proposal_type ON (proposal.proposal_type_id=proposal_type.id)
                WHERE
                    (
                        SELECT COUNT(review2.id)
                            FROM review as review2
                            WHERE review2.proposal_id = proposal.id
                    ) != 0
                GROUP BY proposal.id, proposal.title, review.score, proposal_type.name
                ORDER BY proposal_type.name ASC, review.score DESC, "#reviewers at this score / #total reviews %%" DESC, proposal.id ASC"""

        return sql_response(query)

    @authorize(h.auth.has_reviewer_role)
    def proposals_by_max_rank(self):
        """ List of all the proposals ordered max score, min score then average [CFP] """
        return sql_response("""
                SELECT
                    proposal.id,
                    proposal.title,
                    proposal_type.name AS "proposal type",
                    MAX(review.score) AS max,
                    MIN(review.score) AS min,
                    ROUND(AVG(review.score),2) AS avg
                FROM proposal
                    LEFT JOIN review ON (proposal.id=review.proposal_id)
                    LEFT JOIN proposal_type ON (proposal.proposal_type_id=proposal_type.id)
                GROUP BY proposal.id, proposal.title, proposal_type.name
                ORDER BY proposal_type.name ASC, max DESC, min DESC, avg DESC, proposal.id ASC
                """)

    @authorize(h.auth.has_reviewer_role)
    def proposals_by_stream(self):
        """ List of all the proposals ordered by stream, max score, min score then average [CFP] """
        return sql_response("""
                SELECT
                    proposal.id,
                    proposal.title,
                    proposal_type.name AS "proposal type",
                    stream.name AS stream,
                    MAX(review.score) AS max,
                    MIN(review.score) AS min,
                    ROUND(AVG(review.score),2) AS avg
                FROM proposal
                    LEFT JOIN review ON (proposal.id=review.proposal_id)
                    LEFT JOIN proposal_type ON (proposal.proposal_type_id=proposal_type.id)
                    LEFT JOIN stream ON (review.stream_id=stream.id)
                WHERE review.stream_id = (SELECT review2.stream_id FROM review review2 WHERE review2.proposal_id = proposal.id GROUP BY review2.stream_id ORDER BY count(review2.stream_id) DESC LIMIT 1)
                GROUP BY proposal.id, proposal.title, proposal_type.name, stream.name
                ORDER BY stream.name, proposal_type.name ASC, max DESC, min DESC, avg DESC, proposal.id ASC
                """)

    @authorize(h.auth.has_reviewer_role)
    def proposals_by_number_of_reviewers(self):
        """ List of all proposals ordered by number of reviewers [CFP] """
        return sql_response("""
                SELECT
                    proposal.id,
                    proposal.title,
                    proposal_type.name AS "proposal type",
                    COUNT(review.id) AS "reviewers"
                FROM proposal
                    LEFT JOIN review ON (proposal.id=review.proposal_id)
                    LEFT JOIN proposal_type ON (proposal.proposal_type_id=proposal_type.id)
                GROUP BY proposal.id, proposal.title, proposal_type.name
                ORDER BY reviewers ASC, proposal.id ASC
                """)

    @authorize(h.auth.has_reviewer_role)
    def proposals_by_date(self):
        """ List of proposals by date submitted [CFP] """
        return sql_response("""
                SELECT
                    proposal.id,
                    proposal.title,
                    proposal_type.name AS "proposal type",
                    proposal.creation_timestamp AS "submitted"
                FROM proposal
                    LEFT JOIN proposal_type ON (proposal.proposal_type_id=proposal_type.id)
                ORDER BY proposal.creation_timestamp ASC, proposal.id ASC
                """)

    @authorize(h.auth.has_funding_reviewer_role)
    def funding_requests_by_strong_rank(self):
        """ List of funding applications ordered by number of certain score / total number of reviewers [Funding] """
        query = """
                SELECT
                    funding.id,
                    person.firstname || ' ' || person.lastname AS fullname,
                    funding_type.name AS "funding type",
                    funding_review.score,
                    COUNT(funding_review.id) AS "#reviewers at this score",
                    (
                        SELECT COUNT(review2.id)
                            FROM funding_review as review2
                            WHERE review2.funding_id = funding.id
                    ) AS "#total reviewers",
                    CAST(
                        CAST(
                            COUNT(funding_review.id) AS float(8)
                        ) / CAST(
                            (SELECT COUNT(review2.id)
                                FROM funding_review as review2
                                WHERE review2.funding_id = funding.id
                            ) AS float(8)
                        ) AS float(8)
                    ) AS "#reviewers at this score / #total reviews %%"
                FROM funding
                    LEFT JOIN funding_review ON (funding.id=funding_review.funding_id)
                    LEFT JOIN funding_type ON (funding.funding_type_id=funding_type.id)
                    LEFT JOIN person ON (funding.person_id=person.id)
                WHERE
                    (
                        SELECT COUNT(review2.id)
                            FROM funding_review as review2
                            WHERE review2.funding_id = funding.id
                    ) != 0
                GROUP BY funding.id, fullname, funding_review.score, funding_type.name
                ORDER BY funding_type.name ASC, funding_review.score DESC, "#reviewers at this score / #total reviews %%" DESC, funding.id ASC"""

        return sql_response(query)

    @authorize(h.auth.has_funding_reviewer_role)
    def funding_requests_by_max_rank(self):
        """ List of all the funding applications ordered max score, min score then average [Funding] """
        return sql_response("""
                SELECT
                    funding.id,
                    person.firstname || ' ' || person.lastname AS fullname,
                    funding_type.name AS "funding type",
                    MAX(funding_review.score) AS max,
                    MIN(funding_review.score) AS min,
                    ROUND(AVG(funding_review.score),2) AS avg
                FROM funding
                    LEFT JOIN funding_review ON (funding.id=funding_review.funding_id)
                    LEFT JOIN funding_type ON (funding.funding_type_id=funding_type.id)
                    LEFT JOIN person ON (funding.person_id=person.id)
                GROUP BY funding.id, fullname, funding_type.name
                ORDER BY funding_type.name ASC, max DESC, min DESC, avg DESC, funding.id ASC
                """)

    @authorize(h.auth.has_organiser_role)
    def _countdown(self):
        """ How many days until conference opens """
        timeleft = lca_info['date'] - datetime.now()
        c.text = "%.1f days" % (timeleft.days +
                                               timeleft.seconds / (3600*24.))
        return render('/admin/text.mako')

    @authorize(h.auth.has_organiser_role)
    def silly_description_checksum(self):
        """ Generate the checksum for a given silly_description [Registrations] """
        if request.GET:
            if request.GET['silly_description']:
                c.silly_description = request.GET['silly_description']
                c.silly_description_checksum = h.silly_description_checksum(c.silly_description)
        return render('/admin/silly_description_checksum.mako')

    @authorize(h.auth.has_organiser_role)
    def registered_followup(self):
        """ CSV export of registrations for mail merges [Registrations] """
        c.data = []
        c.text = ''
        c.columns = ('id', 'name', 'firstname', 'email_address', 'country', 'speaker', 'keynote', 'dietary_requirements', 'special_requirements', 'paid')
        c.noescape = True
        for r in meta.Session.query(Registration).all():
          # We only care about people that have valid invoices.
          if not r.person.has_valid_invoice():
            continue

          row = []
          row.append(str(r.person.id))
          row.append(r.person.fullname)
          row.append(r.person.firstname)
          row.append(r.person.email_address)
          row.append(r.person.country)
          if r.person.is_speaker():
            row.append('Yes')
          else:
            row.append('No')
          row.append('No')
          if r.person.is_miniconf_org():
            row.append('Yes')
          else:
            row.append('No')
          row.append(r.diet)
          row.append(r.special)
          if r.person.paid():
            row.append('Yes')
          else:
            row.append('No')

          c.data.append(row)
        return table_response()

    @authorize(h.auth.has_organiser_role)
    def registered_speakers(self):
        """ Listing of speakers and various stuff about them [Speakers] """
        """ HACK: This code should be in the registration controller """
        import re
        shirt_totals = {}
        c.data = []
        c.noescape = True
        cons_list = ('video_release', 'slides_release')
        speaker_list = [p for p in meta.Session.query(Person).order_by(Person.lastname, Person.firstname).all() if p.is_speaker() or p.is_miniconf_org()]

        for p in speaker_list:
            res = []
            res.append(h.link_to(p.fullname, url=h.url_for(controller='person', action='view', id=p.id)))
            res.append(h.link_to(p.email_address, url='mailto:' + p.email_address))
            res.append('; '.join([h.link_to(h.truncate(t.title), url=h.url_for(controller='schedule', action='view_talk', id=t.id)) for t in p.proposals if t.accepted]))
            if p.registration:
                res.append(h.link_to(p.registration.id, url=h.url_for(controller='registration', action='view', id=p.registration.id)))
                if p.invoices:
                    if p.valid_invoice() is None:
                        res.append('Invalid Invoice')
                    else:
                        if p.valid_invoice().is_paid:
                            res.append(h.link_to('Paid ' + h.integer_to_currency(p.valid_invoice().total),
                                           url=h.url_for(controller='invoice', action='view', id=p.valid_invoice().id)))
                        else:
                            res.append(h.link_to('Owes ' + h.integer_to_currency(p.valid_invoice().total),
                                           url=h.url_for(controller='invoice', action='view', id=p.valid_invoice().id)))

                        shirt = ''
                        for item in p.valid_invoice().items:
                            if ((item.description.lower().find('shirt') is not -1) and (item.description.lower().find('discount') is -1)):
                                shirt += item.description + ', '
                                if shirt_totals.has_key(item.description):
                                    shirt_totals[item.description] += 1
                                else:
                                    shirt_totals[item.description] = 1
                        res.append(shirt)
                else:
                    res.append('No Invoice')
                    res.append('-')

            else:
                res+=['Not Registered', '', '']

            consents = []
            talks = [talk for talk in p.proposals if talk.accepted]
            for t in talks:
                cons = [con.replace('_', ' ') for con in cons_list if getattr(t, con)]
                if len(cons)==len(cons_list):
                    consents.append('Release All')
                elif len(cons)==0:
                    consents.append('None')
                else:
                    consents.append(' and '.join(cons))
            res.append(';'.join(consents))

            if p.registration:
                res.append('<br><br>'.join(["<b>Note by <i>" + n.by.firstname + " " + n.by.lastname + "</i> at <i>" + n.last_modification_timestamp.strftime("%Y-%m-%d&nbsp;%H:%M") + "</i>:</b><br>" + h.line_break(n.note) for n in p.registration.notes]))
                if p.registration.diet:
                    res[-1] += '<br><br><b>Diet:</b> %s' % (p.registration.diet)
                if p.registration.special:
                    res[-1] += '<br><br><b>Special Needs:</b> %s' % (p.registration.special)
            else:
                res.append('')

            c.data.append(res)

        # sort by rego status (while that's important)
        def my_cmp(a,b):
            return cmp(a[2], b[2])
        c.data.sort(my_cmp)

        c.columns = ('Name', 'Email', 'Talk(s)', 'Registration', 'Status', 'Shirts', 'Concent', 'Notes')
        c.text = "<p>Shirt Totals:"
        for key, value in shirt_totals.items():
            c.text += "<br>" + str(key) + ": " + str(value)
        c.text += "</p>"
        return table_response()

    @authorize(h.auth.has_organiser_role)
    def registered_volunteers(self):
        """ Listing of volunteers and various stuff about them [Speakers] """
        """ HACK: This code should be in the registration controller """
        import re
        shirt_totals = {}
        c.data = []
        c.noescape = True
        volunteer_list = []
        for p in meta.Session.query(Person).all():
            if not p.is_volunteer(): continue
            volunteer_list.append((p.lastname.lower()+' '+p.firstname, p))
        volunteer_list.sort()

        for (sortkey, p) in volunteer_list:
            registration_link = ''
            if p.registration:
                registration_link = '<a href="/registration/%d">Details</a>, ' % (p.registration.id)
            res = [
      '<a href="/person/%d">%s %s</a> (%s<a href="mailto:%s">email</a>)'
                  % (p.id, p.firstname, p.lastname, registration_link, p.email_address)
            ]

            if p.registration:
              if p.invoices:
                if p.valid_invoice() is None:
                    res.append('Invalid Invoice')
                else:
                    if p.valid_invoice().is_paid:
                      res.append(h.link_to('Paid ' + h.integer_to_currency(p.valid_invoice().total),
                                           h.url_for(controller='invoice', action='view', id=p.valid_invoice().id)))
                    else:
                      res.append(h.link_to('Owes ' + h.integer_to_currency(p.valid_invoice().total),
                                           h.url_for(controller='invoice', action='view', id=p.valid_invoice().id)))

                    shirt = ''
                    for item in p.valid_invoice().items:
                        if ((item.description.lower().find('shirt') is not -1) and (item.description.lower().find('discount') is -1)):
                            shirt += item.description + ', '
                            if shirt_totals.has_key(item.description):
                                shirt_totals[item.description] += 1
                            else:
                                shirt_totals[item.description] = 1
                    res.append(shirt)
              else:
                res.append('No Invoice')
                res.append('-')

              res.append('<br><br>'.join(["<b>Note by <i>" + n.by.firstname + " " + n.by.lastname + "</i> at <i>" + n.last_modification_timestamp.strftime("%Y-%m-%d&nbsp;%H:%M") + "</i>:</b><br>" + h.line_break(n.note) for n in p.registration.notes]))
              if p.registration.diet:
                  res[-1] += '<br><br><b>Diet:</b> %s' % (p.registration.diet)
              if p.registration.special:
                  res[-1] += '<br><br><b>Special Needs:</b> %s' % (p.registration.special)
            else:
              res+=['Not Registered', '', '', '']
            #res.append(`dir(p.registration)`)
            c.data.append(res)

        # sort by rego status (while that's important)
        def my_cmp(a,b):
            return cmp(a[1], b[1])
        c.data.sort(my_cmp)

        c.columns = ('Name', 'Status', 'Shirts', 'Notes')
        c.text = "<p>Shirt Totals:"
        for key, value in shirt_totals.items():
            c.text += "<br>" + str(key) + ": " + str(value)
        c.text += "</p>"
        return table_response()

    @authorize(h.auth.has_organiser_role)
    def registered_parking(self):
        """ List of people with parking requested [Registration] """
        return sql_response("""
            SELECT
                person.id AS person_id,
                person.firstname,
                person.lastname,
                person.email_address,
                ceiling.name AS ceiling,
                invoice_item.description,
                SUM(invoice_item.qty) AS qty
            FROM person
            JOIN invoice ON (person.id=invoice.person_id)
            JOIN invoice_item ON (invoice.id=invoice_item.invoice_id)
            JOIN product ON (invoice_item.product_id=product.id)
            JOIN product_ceiling_map ON (product.id=product_ceiling_map.product_id)
            JOIN ceiling ON (product_ceiling_map.ceiling_id=ceiling.id)
            WHERE (
                (
                    invoice.void IS NULL AND (
                        SELECT CASE WHEN (count(invoice_item.id) = 0) THEN 0 ELSE sum(invoice_item.cost * invoice_item.qty) END AS anon_7 
                        FROM invoice_item 
                        WHERE invoice_item.invoice_id = invoice.id
                    ) = (
                        SELECT CASE WHEN (count(payment_received.id) = 0) THEN 0 ELSE sum(payment_received.amount_paid) END AS anon_8 
                        FROM payment_received 
                        WHERE payment_received.invoice_id = invoice.id AND payment_received.approved = '1'
                    )
                ) = 't'
            )
            AND ceiling.name = 'parking-all'
            GROUP BY person.id, person.firstname, person.lastname, person.email_address, invoice_item.description, ceiling.name
            HAVING SUM(invoice_item.qty) != 0
            ORDER BY ceiling.name, invoice_item.description;
        """)

    @authorize(h.auth.has_organiser_role)
    def registered_accommodation(self):
        """ List of people with accommodation requested [Registration] """
        return sql_response("""
            SELECT
                person.id AS person_id,
                person.firstname,
                person.lastname,
                person.email_address,
                registration.special,
                registration.diet,
                ceiling.name AS ceiling,
                invoice_item.description,
                SUM(invoice_item.qty) AS qty
            FROM person
            LEFT OUTER JOIN registration ON (person.id=registration.person_id)
            JOIN invoice ON (person.id=invoice.person_id)
            JOIN invoice_item ON (invoice.id=invoice_item.invoice_id)
            JOIN product ON (invoice_item.product_id=product.id)
            JOIN product_ceiling_map ON (product.id=product_ceiling_map.product_id)
            JOIN ceiling ON (product_ceiling_map.ceiling_id=ceiling.id)
            WHERE (
                (
                    invoice.void IS NULL AND (
                        SELECT CASE WHEN (count(invoice_item.id) = 0) THEN 0 ELSE sum(invoice_item.cost * invoice_item.qty) END AS anon_7 
                        FROM invoice_item 
                        WHERE invoice_item.invoice_id = invoice.id
                    ) = (
                        SELECT CASE WHEN (count(payment_received.id) = 0) THEN 0 ELSE sum(payment_received.amount_paid) END AS anon_8 
                        FROM payment_received 
                        WHERE payment_received.invoice_id = invoice.id AND payment_received.approved = '1'
                    )
                ) = 't'
            )
            AND ceiling.name = 'accom-all'
            GROUP BY person.id, person.firstname, person.lastname, person.email_address, invoice_item.description, ceiling.name, registration.special, registration.diet
            HAVING SUM(invoice_item.qty) != 0
            ORDER BY ceiling.name, invoice_item.description;
        """)

    @authorize(h.auth.has_organiser_role)
    def registered_without_accom(self):
        """ List of people with accommodation requested [Registration] """
        return sql_response("""
            SELECT person.id, person.firstname, person.lastname, person.email_address, person.country, person.state
            FROM person
            JOIN registration ON (person.id=registration.person_id)
            WHERE (
                (country = 'AUSTRALIA' AND state != 'ACT')
                OR country != 'AUSTRALIA'
            ) AND (
                person.id NOT IN (
                    SELECT person_id
                    FROM invoice
                    JOIN invoice_item ON (invoice.id=invoice_item.invoice_id)
                    JOIN product_ceiling_map ON (invoice_item.product_id = product_ceiling_map.product_id)
                    WHERE product_ceiling_map.ceiling_id = 19
               )
            );
        """)

    @authorize(h.auth.has_organiser_role)
    def reconcile(self):
        """ Reconcilliation between D1 and ZK; for now, compare the D1 data
        that have been placed in the fixed location in the filesystem and
        work from there... [Invoicing] """
        import csv
        d1_data = csv.reader(file('/srv/zkpylons/reconcile.d1'))
        d1_cols = d1_data.next()
        d1_cols = [s.strip() for s in d1_cols]

        all = {}

        t_offs = d1_cols.index('payment_id')
        t_offs = d1_cols.index('invoice_reference')
        amt_offs = d1_cols.index('payment_amount')
        d1 = {}
        x=1
        for row in d1_data:
          t = row[t_offs]
          # The invoice reference (t) takes the form "lca2012 i-18 p-11"
          # We only want the i value so strip the rest off
          t = t.strip("lca2012 i")
          t = t.strip("-")
          t = int(t.split(" ")[0])

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
          x = x + 1
        #c.data = d1

        zk = {}
        for p in meta.Session.query(PaymentReceived).all():
          t = p.payment_id
          t = p.invoice_id
          all[t] = 1
          if zk.has_key(t):
            zk[t].append(p)
          else:
            zk[t] = [p]

        zk_fields =  ('invoice_id', 'payment_id', 'amount_paid', 'response_text', 'success_code')
        all = all.keys()
        all.sort()
        c.data = []
        for t in all:
          zk_t = zk.get(t, []); d1_t = d1.get(t, [])
          if len(zk_t)==1 and len(d1_t)==1:
            if str(zk_t[0].amount_paid) == d1_t[0][-1]:
              continue
          c.data.append((
            '; '.join([', '.join([str(getattr(z, f)) for f in zk_fields])
                                                              for z in zk_t]),
            t,
            '; '.join([', '.join(d) for d in d1_t])
          ))

        return table_response()

    @authorize(h.auth.has_organiser_role)
    def linux_australia_signup(self):
        """ People who ticked "I want to sign up for (free) Linux Australia
        membership!" [Mailing Lists] """

        c.text = """<p>People who ticked "I want to sign up for (free) Linux
        Australia membership!" (whether or not they then went on to pay for
        the conference).</p>"""

        query = """SELECT person.firstname, person.lastname, person.email_address,
                    person.address1, person.address2, person.city, person.state, person.postcode, person.country,
                    person.phone, person.mobile, person.company,
                    registration.creation_timestamp
                   FROM person
                   LEFT JOIN registration ON (person.id = registration.person_id)
                   WHERE registration.signup LIKE '%linuxaustralia%'
                """

        return sql_response(query)

    @authorize(h.auth.has_organiser_role)
    def lca_announce_signup(self):
        """ People who ticked "I want to sign up to the low traffic conference announcement mailing list!" [Mailing Lists] """

        c.text = """<p>People who ticked "I want to sign up to the low traffic conference
        announcement mailing list!" (whether or not they then went on to pay for
        the conference).</p><p>Copy and paste the following into mailman</p>
        <p><textarea cols="100" rows="25">"""

        count = 0
        for r in meta.Session.query(Registration).filter(Registration.signup.like("%announce%")).all():
            p = r.person
            c.text += p.firstname + " " + p.lastname + " &lt;" + p.email_address + "&gt;\n"
            count += 1
        c.text += "</textarea></p>"
        c.text += "<p>Total addresses: " + str(count) + "</p>"

        return render('admin/text.mako')

    @authorize(h.auth.has_organiser_role)
    def lca_chat_signup(self):
        """ People who ticked "I want to sign up to the conference attendees mailing list!" [Mailing Lists] """

        c.text = """<p>People who ticked "I want to sign up to the conference attendees mailing list!" (whether or not they then went on to pay for
        the conference).</p><p>Copy and paste the following into mailman</p>
        <p><textarea cols="100" rows="25">"""

        count = 0
        for r in meta.Session.query(Registration).filter(Registration.signup.like('%chat%')).all():
            p = r.person
            c.text += p.firstname + " " + p.lastname + " &lt;" + p.email_address + "&gt;\n"
            count += 1
        c.text += "</textarea></p>"
        c.text += "<p>Total addresses: " + str(count) + "</p>"

        return render('admin/text.mako')

    @authorize(h.auth.has_organiser_role)
    def partners_programme_signup(self):
        """ List of partners programme people for mailing list [Mailing Lists] """
        c.text = """<p>Partners Programme people.  If they don't have an email address listed, then we'll use the person actually registered for the conference.</p>
        <p>Copy and paste the following into mailman</p>
        <p><textarea cols="100" rows="25">"""

        count = 0
        partners_list = meta.Session.query(Product).filter(Product.category.has(name = 'Partners\' Programme')).all()

        for item in partners_list:
            for invoice_item in item.invoice_items:
                if invoice_item.invoice.is_paid and not invoice_item.invoice.is_void:
                    r = invoice_item.invoice.person.registration
                    if r.partner_email is not None:
                        c.text += r.partner_name + " &lt;" + r.partner_email + "&gt;\n"
                    elif r.partner_name is not None:
                        c.text += r.partner_name + " &lt;" + r.person.email_address + "&gt;\n"
                    else:
                        c.text += r.person.fullname + " &lt;" + r.person.email_address + "&gt;\n"
                    count += 1
        c.text += "</textarea></p>"
        c.text += "<p>Total addresses: " + str(count) + "</p>"

        return table_response()

    @authorize(h.auth.has_organiser_role)
    def speakers_partners(self):
        """ Listing of speakers and their partner details [Speakers] """
        c.columns = ['Speaker', 'e-mail', 'Partners\' Programme', 'Penguin Dinner']
        c.data = []

        total_partners = 0
        total_dinner = 0
        speakers_count = 0
        for person in meta.Session.query(Person).all():
            partners = []
            dinner_tickets = 0
            if person.is_speaker():
                for invoice in person.invoices:
                    for item in invoice.items:
                        if item.product is not None:
                            if item.product.category.name == "Partners' Programme":
                                partners.append(item.description + " x" + str(item.qty))
                                total_partners += item.qty
                            if item.product.category.name == "Penguin Dinner":
                                dinner_tickets += item.qty
                                total_dinner += item.qty
                c.data.append([person.fullname,
                               person.email_address,
                               ", ".join(partners),
                               str(dinner_tickets)])
                speakers_count += 1
        c.data.append(['TOTALS:', str(speakers_count) + ' speakers', str(total_partners) + ' partners', str(total_dinner) + ' dinner tickets'])
        return table_response()

    @authorize(h.auth.has_organiser_role)
    def talks(self):
        """ List of talks for use in programme printing [Schedule] """
        c.text = "Talks with multiple speakers will appear twice."
        query = """SELECT proposal_type.name AS type, proposal.title, proposal.abstract, person.firstname || ' ' || person.lastname as speaker, person.bio
                    FROM proposal
                    LEFT JOIN person_proposal_map ON (person_proposal_map.proposal_id = proposal.id)
                    LEFT JOIN person ON (person_proposal_map.person_id = person.id)
                    LEFT JOIN proposal_type ON (proposal_type.id = proposal.proposal_type_id)
                    LEFT JOIN proposal_status ON (proposal_status.id = proposal.status_id)
                    WHERE proposal_status.name = 'Accepted'
                    ORDER BY proposal_type.name, proposal.title
        """
        return sql_response(query)

    @authorize(h.auth.has_organiser_role)
    def zkpylons_sales(self):
        """ List of products and qty sold. [Inventory] """
        item_list = meta.Session.query(InvoiceItem).all()
        total = 0
        c.columns = ['Item', 'Price', 'Qty', 'Amount']
        c.data = []
        for item in item_list:
            if item.invoice.is_paid and not item.invoice.is_void:
                c.data.append([item.description, h.integer_to_currency(item.cost), item.qty, h.integer_to_currency(item.total)])
                total += item.total
        c.data.append(['','','Total:', h.integer_to_currency(total)])
        return table_response()

    @authorize(h.auth.has_organiser_role)
    def partners_programme(self):
        """ List of partners programme contacts [Partners Programme] """
        partners_list = meta.Session.query(Product).filter(Product.category.has(name = 'Partners\' Programme')).all()
        c.text = "*Checkin and checkout dates aren't an accurate source."
        #c.columns = ['Partner Type', 'Qty', 'Registration Name', 'Registration e-mail', 'Partners name', 'Partners e-mail', 'Partners mobile', 'Checkin*', 'Checkout*']
        c.columns = ['Partner Type', 'Qty', 'Registration Name', 'Registration e-mail', 'Partners name', 'Partners e-mail', 'Partners mobile']
        c.data = []
        for item in partners_list:
            for invoice_item in item.invoice_items:
                if invoice_item.invoice.is_paid and not invoice_item.invoice.is_void:
                    c.data.append([item.description,
                                   invoice_item.qty,
                                   invoice_item.invoice.person.firstname + " " + invoice_item.invoice.person.lastname,
                                   invoice_item.invoice.person.email_address,
                                   invoice_item.invoice.person.registration.partner_name,
                                   invoice_item.invoice.person.registration.partner_email,
                                   invoice_item.invoice.person.registration.partner_mobile,
                                   #invoice_item.invoice.person.registration.checkin,
                                   #invoice_item.invoice.person.registration.checkout
                                 ])
        return table_response()

    @authorize(h.auth.has_organiser_role)
    def planet_lca(self):
        """ List of blog RSS feeds, planet compatible. [Mailing Lists] """
        c.text = """<p>List of RSS feeds for LCA planet.</p>
        <p><textarea cols="100" rows="25">"""

        count = 0
        for r in meta.Session.query(Registration).filter(Registration.planetfeed != '').all():
            p = r.person
            c.text += "[" + r.planetfeed + "] name = " + p.firstname + " " + p.lastname + "\n"
            count += 1
        c.text += "</textarea></p>"
        c.text += "<p>Total addresses: " + str(count) + "</p>"

        return render('admin/text.mako')

    @authorize(h.auth.has_organiser_role)
    def nonregistered(self):
        """ List of people with accounts on the website but who haven't started the registration process for the conference [Accounts] """
        query = """SELECT person.firstname || ' ' || person.lastname as name, person.email_address
                    FROM person
                   WHERE person.id NOT IN (SELECT registration.person_id FROM registration)
        """
        return sql_response(query)

    @authorize(h.auth.Or(h.auth.has_keysigning_role, h.auth.has_organiser_role))
    def _keysigning_participants_list(self):
        """ Generate a list of all current key id's [Keysigning] """
        from pylons import response
        response.headers['Content-type'] = 'text/plain'
        for keyid in self.keysigning_participants():
            response.content.append(keyid + "\n")
        return response

    @authorize(h.auth.Or(h.auth.has_keysigning_role, h.auth.has_organiser_role))
    def _keysigning_single(self):
        """ Generate an A4 page of key fingerprints given a keyid [Keysigning] """
        if request.POST:
            keyid = request.POST['keyid']
            from pylons import response
            response.headers['Content-type'] = 'application/octet-stream'
            response.headers['Content-Disposition'] = ('attachment; filename=%s.pdf' %  keyid)
            pdf = keysigning_pdf(keyid)
            pdf_f = file(pdf)
            response.content = pdf_f.read()
            pdf_f.close()
        else:
            return render('/admin/keysigning_single.mako')

    @authorize(h.auth.Or(h.auth.has_keysigning_role, h.auth.has_organiser_role))
    def _keysigning_conference(self):
        """ Generate an A4 page of key fingerprints for everyone who has provided their fingerprint [Keysigning] """
        import os, tempfile
        (pdf_fd, pdf) = tempfile.mkstemp('.pdf')
        input_pdf = list()
        for keyid in self.keysigning_participants():
            input_pdf.append(keysigning_pdf(keyid))
        os.system('gs -dNOPAUSE -sDEVICE=pdfwrite -sOUTPUTFILE=' + pdf + ' -dBATCH ' + ' '.join(input_pdf))
        from pylons import response
        response.headers['Content-type'] = 'application/octet-stream'
        response.headers['Content-Disposition'] = ('attachment; filename=conference.pdf')
        pdf_f = file(pdf)
        response.content = pdf_f.read()
        pdf_f.close()

    @authorize(h.auth.has_organiser_role)
    def _keysigning_participants(self):
        registration_list = meta.Session.query(Registration).join('person').filter(Registration.keyid != None).filter(Registration.keyid != '').order_by(Person.lastname).all()
        key_list = list()
        for registration in registration_list:
            if registration.person.has_paid_ticket():
                key_list.append(registration.keyid)
        return key_list

    @authorize(h.auth.has_organiser_role)
    def rego_desk_list(self):
        """ List of people who have not checked in (see checkins table). [Registrations] """
        import zkpylons.model
        checkedin = zkpylons.model.metadata.bind.execute("SELECT person_id FROM checkins WHERE conference IS NOT NULL");
        checkedin_list = checkedin.fetchall()
        registration_list = meta.Session.query(Registration).all()
        c.columns = ['ID', 'Name', 'Type', 'Shirts', 'Dinner Tickets', 'Partners Programme']
        c.data = []
        for registration in registration_list:
            if (registration.person.id not in [id[0] for id in checkedin_list]) and registration.person.has_paid_ticket():
                shirts = []
                dinner_tickets = 0
                ticket_types = []
                partners_programme = []
                for invoice in registration.person.invoices:
                    if invoice.is_paid and not invoice.is_void:
                        for item in invoice.items:
                            if item.description.lower().startswith("discount"):
                                pass
                            elif item.description.lower().find("shirt") > -1:
                                shirts.append(item.description + " x" + str(item.qty))
                            elif item.description.lower().startswith("dinner"):
                                dinner_tickets += item.qty
                            elif item.description.lower().startswith("partners"):
                                partners_programme.append(item.description + " x" + str(item.qty))
                            elif item.description.lower().endswith("ticket") or item.description.lower().startswith("press pass"):
                                ticket_types.append(item.description + " x" + str(item.qty))
                c.data.append([registration.person.id,
                               registration.person.firstname + " " + registration.person.lastname,
                               ", ".join(ticket_types),
                               ", ".join(shirts),
                               dinner_tickets,
                               ", ".join(partners_programme)])

        return table_response()

    @authorize(h.auth.has_organiser_role)
    def previous_years_stats(self):
        """ Details on how many people have come to previous years of LCA. All people - including unpaid [Statistics] """
        registration_list = meta.Session.query(Registration).all()
        c.columns = ['year', 'People']
        c.data = []
        years = {}
        veterans = []
        veterans_lca = []
        for registration in registration_list:
            if type(registration.prevlca) == list:
                for year in registration.prevlca:
                    if years.has_key(year):
                        years[year] += 1
                    else:
                        years[year] = 1
                if len(registration.prevlca) == len(lca_rego['past_confs']):
                    veterans.append(registration.person.firstname + " " + registration.person.lastname)
                elif len(registration.prevlca) == (len(lca_rego['past_confs']) - 1):
                    veterans_lca.append(registration.person.firstname + " " + registration.person.lastname)
        for (year, value) in years.iteritems():
            c.data.append([year, value])

        c.text = '''
          <img float="right" width="400" height="200"
          src="http://chart.apis.google.com/chart?cht=p&chs=400x200&chd=t:%s&chl=%s"><br />
        ''' % (
            ','.join([str(count) for (label, count) in c.data]),
            '|'.join([label for (label, count) in c.data]),
        )
        c.text += "Veterans: " + ", ".join(veterans) + "<br><br>Veterans of LCA (excluding CALU): " + ", ".join(veterans_lca)
        return table_response()

    @authorize(h.auth.has_organiser_role)
    def people_by_country(self):
        """ Registered and paid people by country [Statistics] """
        c.data = meta.Session.query(func.initcap(Person.country), func.count(Person.id)).join(Invoice).join(InvoiceItem).join(Product).join(ProductCategory).filter(Invoice.is_paid == True).filter(ProductCategory.name == "Ticket").group_by(func.initcap(Person.country)).order_by(func.initcap(Person.country)).all()
        c.data.sort(lambda a,b: cmp(b[-1], a[-1]) or cmp(a, b))
        c.text = '''
          <img float="right" width="400" height="200"
          src="http://chart.apis.google.com/chart?cht=p&chs=400x200&chd=t:%s&chl=%s">
        ''' % (
            ','.join([str(count) for (label, count) in c.data]),
            '|'.join([label for (label, count) in c.data]),
        )
        return table_response()

    @authorize(h.auth.has_organiser_role)
    def speakers_by_country(self):
        """ Speakers by country [Statistics] """
        data = {}
        for person in meta.Session.query(Person).all():
            if person.is_speaker():
                country = person.country.capitalize()
                data[country] = data.get(country, 0) + 1
        c.data = data.items()
        c.data.sort(lambda a,b: cmp(b[-1], a[-1]) or cmp(a, b))
        c.text = '''
          <img float="right" width="400" height="200"
          src="http://chart.apis.google.com/chart?cht=p&chs=400x200&chd=t:%s&chl=%s">
        ''' % (
            ','.join([str(count) for (label, count) in c.data]),
            '|'.join([label for (label, count) in c.data]),
        )
        return table_response()

    @authorize(h.auth.has_organiser_role)
    def people_by_state(self):
        """ Registered and paid people by state - Australia Only [Statistics] """
        c.data = meta.Session.query(func.initcap(Person.state), func.count(Person.id)).join(Invoice).join(InvoiceItem).join(Product).join(ProductCategory).filter(func.initcap(Person.country) == "Australia").filter(Invoice.is_paid == True).filter(ProductCategory.name == "Ticket").group_by(func.initcap(Person.state)).order_by(func.initcap(Person.state)).all()
        c.data.sort(lambda a,b: cmp(b[-1], a[-1]) or cmp(a, b))
        c.text = '''
          <img float="right" width="400" height="200"
          src="http://chart.apis.google.com/chart?cht=p&chs=400x200&chd=t:%s&chl=%s">
        ''' % (
            ','.join([str(count) for (label, count) in c.data]),
            '|'.join([label for (label, count) in c.data]),
        )
        return table_response()

    @authorize(h.auth.has_organiser_role)
    def favourite_distro(self):
        """ Statistics on favourite distros. All people - including unpaid [Statistics] """
        data = {}
        for registration in meta.Session.query(Registration).all():
            distro = registration.distro.capitalize()
            data[distro] = data.get(distro, 0) + 1
        c.data = data.items()
        c.data.sort(lambda a,b: cmp(b[-1], a[-1]) or cmp(a, b))
        c.text = '''
          <img float="right" width="400" height="200"
          src="http://chart.apis.google.com/chart?cht=p&chs=400x200&chd=t:%s&chl=%s">
        ''' % (
            ','.join([str(count) for (label, count) in c.data]),
            '|'.join([label for (label, count) in c.data]),
        )
        return table_response()

    @authorize(h.auth.has_organiser_role)
    def favourite_editor(self):
        """ Statistics on favourite editors. All people - including unpaid [Statistics] """
        data = {}
        for registration in meta.Session.query(Registration).all():
            editor = registration.editor.capitalize()
            data[editor] = data.get(editor, 0) + 1
        c.data = data.items()
        c.data.sort(lambda a,b: cmp(b[-1], a[-1]) or cmp(a, b))
        c.text = '''
          <img float="right" width="400" height="200"
          src="http://chart.apis.google.com/chart?cht=p&chs=400x200&chd=t:%s&chl=%s">
        ''' % (
            ','.join([str(count) for (label, count) in c.data]),
            '|'.join([label for (label, count) in c.data]),
        )
        return table_response()

    @authorize(h.auth.has_organiser_role)
    def favourite_shell(self):
        """ Statistics on favourite shells. All people - including unpaid [Statistics] """
        data = {}
        for registration in meta.Session.query(Registration).all():
            shell = registration.shell.capitalize()
            data[shell] = data.get(shell, 0) + 1
        c.data = data.items()
        c.data.sort(lambda a,b: cmp(b[-1], a[-1]) or cmp(a, b))
        c.text = '''
          <img float="right" width="400" height="200"
          src="http://chart.apis.google.com/chart?cht=p&chs=400x200&chd=t:%s&chl=%s">
        ''' % (
            ','.join([str(count) for (label, count) in c.data]),
            '|'.join([label for (label, count) in c.data]),
        )
        return table_response()

    @authorize(h.auth.has_organiser_role)
    def favourite_vcs(self):
        """ Statistics on favourite vcs. All people - including unpaid [Statistics] """
        data = {}
        for registration in meta.Session.query(Registration).all():
            vcs = registration.vcs.capitalize()
            data[vcs] = data.get(vcs, 0) + 1
        c.data = data.items()
        c.data.sort(lambda a,b: cmp(b[-1], a[-1]) or cmp(a, b))
        c.text = '''
          <img float="right" width="400" height="200"
          src="http://chart.apis.google.com/chart?cht=p&chs=400x200&chd=t:%s&chl=%s">
        ''' % (
            ','.join([str(count) for (label, count) in c.data]),
            '|'.join([label for (label, count) in c.data]),
        )
        return table_response()

    @authorize(h.auth.has_organiser_role)
    def email_registration_reminder(self):
        """ Send all attendees a confirmation email of their registration details. [Registrations]"""
        c.text = 'Emailed the following attendees:'
        c.columns = ['Full name', 'Email address']
        c.data = []

        for p in self.dbsession.query(Person).all():
            # Make sure the person has paid
            if not p.paid():
                continue

            # Don't send a reminder if one has been sent already
            if p.registration.reminder_timestamp is not None:
                continue

            c.speaker = p.is_speaker()
            c.firstname = p.firstname
            c.fullname = p.firstname + ' ' + p.lastname
            c.company = p.company
            c.phone = p.phone
            c.mobile = p.mobile
            c.email = p.email_address
            c.address = p.address1
            if len(p.address2) > 0:
                c.address += + '\n            ' + p.address2
            c.address += '\n            ' + p.city
            if len(p.state) > 0:
                c.address += ', ' + p.state
            if len(p.postcode) > 0:
                c.address += ' ' + p.postcode
            c.address += '\n            ' + p.country

            msg = render('registration/email_reminder.myt', fragment=True)
            email(c.email, msg)
            # keep track of the time this person was reminded
            p.registration.reminder_timestamp = datetime.now()
            c.data.append([c.fullname, c.email])

        self.dbsession.flush()
        c.text = render_response('admin/table.myt', fragment=True)
        return render_response('admin/text.myt')

    @authorize(h.auth.has_organiser_role)
    def late_submitters(self):
        """ List of people who are allowed to submit and edit their proposals after the CFP has closed. [CFP]"""
        c.text = '<p>List of people who are allowed to submit and edit their proposals after the CFP has closed.</p><p><b>The role should be REMOVED once they have submitted their proposal.</b></p>'

        query = """SELECT p.id, p.firstname || ' ' || p.lastname as name, p.email_address,
                          (SELECT count(*)
                             FROM person_proposal_map ppm
                            WHERE ppm.person_id = p.id) AS number_proposals
                    FROM person p
                    JOIN person_role_map prm ON p.id = prm.person_id
                    JOIN role r ON prm.role_id = r.id
                   WHERE r.name = 'late_submitter'
                ORDER BY number_proposals DESC, p.id
        """
        res = meta.Session.execute(query)
        c.columns = get_column_names(res)
        c.data = []
        for r in res.fetchall():
            idlink = '<a href="/person/' + str(r[0]) + '/roles">' + str(r[0]) + '</a>'
            c.data.append([ idlink, h.util.html_escape(r[1]), h.util.html_escape(r[2]), str(r[3]) ])
        c.noescape = True
        c.sql = query
        return table_response()

    @authorize(h.auth.has_organiser_role)
    def rego_foreign(self):
        people = [ r.person for r in Registration.find_all() ]
        c.columns = ['Name', 'Country']
        c.data = []
        for person in people:
            if person.country != 'AUSTRALIA' and person.paid():
                row = [ "%s %s" % (person.firstname, person.lastname), person.country ]
                c.data.append(row)
        return table_response()


    @authorize(h.auth.has_organiser_role)
    def rego_list(self):
        """ List of paid regos - for rego desk. [Registrations] """
        people = [
           (r.person.lastname.lower(), r.person.firstname.lower(), r.id, r.person)
                                                 for r in Registration.find_all()]
        people.sort()
        people = [row[-1] for row in people]

        # Find the categories that we display in the rego list.
        categories = []
        for category in ProductCategory.find_all():
          name = category.name
          if name != 'Ticket':
            if name != 'Accommodation' or not (name == 'Accommodation' and (len(category.products) == 0 or (len(category.products) == 1 and category.products[0].cost == 0))):
              categories.append(category.name)
        categories.sort()

        c.columns = ['Name', '', 'ID', 'Ticket', 'Bag']
        for cat in categories:
          c.columns.append(cat)

        c.data = []
        for person in people:
          row = [ "%s, %s" % (person.lastname, person.firstname) ]
          not_paid = ''
          if not person.paid():
            not_paid = '{\\bf NOT PAID} \\newline '
          row.append(not_paid + '\\barcode{' + str(person.id) + '}')
          row.append(person.id)

          bag = 'Prof'
          type = []
          if person.is_speaker() and not person.has_role('organiser'):
            type.append('Speaker')
          if person.is_miniconf_org():
            type.append('Minconf Org')
          #if person.is_professional() and not (person.is_speaker() or person.is_miniconf_org() or person.has_role('organiser')):
          #  type.append('Professional')
          if person.has_role('press'):
            type.append('Media')
          if person.has_role('organiser'):
            type.append('Organiser')
          if len(type) == 0:
            ticket = person.ticket_type()
            if ticket is not None:
              ticket = ticket.replace('Earlybird ', '')
              ticket = ticket.replace('Concession/Student', 'Student')
              ticket = ticket.replace('Sponsorship', '')
              type.append(ticket)
            if not person.is_professional():
              bag = 'Hobby'
          if person.is_volunteer() and 'Volunteer' not in type:
            type.append("Volunteer")

          if len(type) > 0:
            row.append(",\\newline ".join(type))
          else:
            row.append("No valid ticket")
          row.append(bag)

          # We only want to put someone on the list if they have valid invoices.
          valid_invoices = False

          first = True
          products = dict()
          for category in categories:
            products[category] = []

          for invoice in person.invoices:
            if not invoice.is_void:
              valid_invoices = True
              for ii in invoice.items:
                if ii.product is not None and ii.product.category is not None:
                  if ii.product.category.name in products:
                    text = "%s x %s" % (ii.qty, ii.product.description)
                    text = text.replace(' years old', '')
#                    if not invoice.is_paid:
#                      text += " (Not paid)"
                    products[ii.product.category.name].append(text)

          for category in categories:
            if len(products[category]) == 0:
              row.append('')
            else:
              row.append(",\\newline ".join(products[category]))

          if valid_invoices:
            c.data.append(row)

        return table_response()

    @authorize(h.auth.has_organiser_role)
    def _volunteer_grid(self):
        """ List of volunteers for exporting to mgmt DB. [Registrations] """
        c.data = []
        c.noescape = True
        c.columns = ['ID', 'Vol ID', 'Name', 'Email', 'Country', 'City', 'Status', 'Type']
        for area in h.lca_rego['volunteer_areas']:
          c.columns.append(area['name'])
        c.columns.append('Other')
        c.columns.append('Experience')

        volunteer_collection = Volunteer.find_all()
        for v in volunteer_collection:
          row = [str(v.person.id)]
          row.append(str(v.id))
          row.append(h.link_to(v.person.fullname, url=h.url_for(controller="person", action='view', id=v.person.id)))
          row.append(h.link_to(v.person.email_address, url="mailto:" + v.person.email_address))
          row.append(v.person.country)
          row.append(v.person.city)
          if v.accepted is None:
            status = 'Pending'
          elif v.accepted == True:
            status = 'Accepted'
          else:
            status = 'Rejected'
          row.append(status)

          type = 'Unknown'
          if v.person.is_speaker():
            type = 'Speaker'
          elif v.person.is_miniconf_org():
            type = 'Miniconf Org'
          else:
            type = 'Not Registered'

            for invoice in v.person.invoices:
              if invoice.is_paid and not invoice.is_void:
                for item in invoice.items:
                  if item.description.find('Volunteer') > -1:
                    type = 'Volunteer'
                  elif item.description.find('Ticket') > -1:
                    type = 'Delegate'

          row.append(type)

          for area in h.lca_rego['volunteer_areas']:
            code = area['name'].replace(' ', '_').replace('.', '_')
            if code in v.areas:
              row.append('Yes')
            else:
              row.append('No')

          row.append(v.other)
          row.append(v.experience)

          c.data.append(row)

        return table_response()

    @authorize(h.auth.has_organiser_role)
    def paid_counts_by_date(self):
        """ Number of paid (or zerod) invoices by date. [Registrations] """
        invoices = Invoice.find_all()

        payments_count = dict()
        for i in invoices:
          if i.is_paid and not i.is_void:
            if i.total == 0:
              date = i.creation_timestamp.date()
            else:
              date = i.good_payments[0].creation_timestamp.date()

            if date not in payments_count:
              payments_count[date] = 0

            payments_count[date] += 1

        c.data = []
        c.noescape = True
        c.columns = ['Date', 'Count' ]
        if len(payments_count) > 0:
          dates = payments_count.keys()
          dates.sort()

          for date in dates:
            row = [ "%s" % date, str(payments_count[date]) ]
            c.data.append(row)

        return table_response()

    @authorize(h.auth.has_organiser_role)
    def paid_product_by_date(self):
        """ Number of paid (actual payments only) invoices per ceiling by date. [Registrations] """
        return sql_response("""
            SELECT
                DATE(payment_received.creation_timestamp) AS date,
                product_category.name,
                product.description AS product,
                SUM(invoice_item.qty - invoice_item.free_qty) AS qty,
                SUM(invoice_item.cost * (invoice_item.qty - invoice_item.free_qty)) / 100 AS total
            FROM payment_received
            JOIN invoice ON (payment_received.invoice_id=invoice.id)
            JOIN invoice_item ON (invoice.id=invoice_item.invoice_id)
            JOIN product ON (invoice_item.product_id = product.id)
            JOIN product_category ON (product.category_id=product_category.id)
            WHERE payment_received.approved = 't'
            GROUP BY product_category.name, product_category.display_order, product.display_order, product.description, DATE(payment_received.creation_timestamp)
            HAVING SUM(invoice_item.qty - invoice_item.free_qty) != 0 AND SUM(invoice_item.cost * (invoice_item.qty - invoice_item.free_qty)) != 0
            ORDER BY product_category.display_order, DATE(payment_received.creation_timestamp), product.display_order;
        """)

    @authorize(h.auth.has_organiser_role)
    def paid_ticket_by_date(self):
        """ Number of paid (actual payments only) invoices per ceiling by date. [Registrations] """
        return sql_response("""
            SELECT
                DATE(payment_received.creation_timestamp) AS date,
                product.description AS product,
                SUM(invoice_item.qty - invoice_item.free_qty) AS qty,
                SUM(invoice_item.cost * (invoice_item.qty - invoice_item.free_qty)) / 100 AS total
            FROM payment_received
            JOIN invoice ON (payment_received.invoice_id=invoice.id)
            JOIN invoice_item ON (invoice.id=invoice_item.invoice_id)
            JOIN product ON (invoice_item.product_id = product.id)
            JOIN product_category ON (product.category_id=product_category.id)
            WHERE payment_received.approved = 't'
            AND product_category.name = 'Ticket'
            GROUP BY product_category.name, product_category.display_order, product.display_order, product.description, DATE(payment_received.creation_timestamp)
            HAVING SUM(invoice_item.qty - invoice_item.free_qty) != 0 AND SUM(invoice_item.cost * (invoice_item.qty - invoice_item.free_qty)) != 0
            ORDER BY product_category.display_order, DATE(payment_received.creation_timestamp), product.display_order;
        """)

    @authorize(h.auth.has_organiser_role)
    def paid_accom_by_date(self):
        """ Number of paid (actual payments only) invoices per ceiling by date. [Registrations] """
        return sql_response("""
            SELECT
                DATE(payment_received.creation_timestamp) AS date,
                product.description AS product,
                SUM(invoice_item.qty - invoice_item.free_qty) AS qty,
                SUM(invoice_item.cost * (invoice_item.qty - invoice_item.free_qty)) / 100 AS total
            FROM payment_received
            JOIN invoice ON (payment_received.invoice_id=invoice.id)
            JOIN invoice_item ON (invoice.id=invoice_item.invoice_id)
            JOIN product ON (invoice_item.product_id = product.id)
            JOIN product_category ON (product.category_id=product_category.id)
            WHERE payment_received.approved = 't'
            AND product_category.name = 'Accommodation'
            GROUP BY product_category.name, product_category.display_order, product.display_order, product.description, DATE(payment_received.creation_timestamp)
            HAVING SUM(invoice_item.qty - invoice_item.free_qty) != 0 AND SUM(invoice_item.cost * (invoice_item.qty - invoice_item.free_qty)) != 0
            ORDER BY product_category.display_order, DATE(payment_received.creation_timestamp), product.display_order;
        """)

    @authorize(h.auth.has_organiser_role)
    def av_norelease(self):
        """ A list of proposals without releases for video/slides [AV] """
        talk_list = Proposal.find_all_accepted().filter(or_(Proposal.video_release==False, Proposal.slides_release==False)).order_by(Proposal.scheduled)

        c.columns = ['Talk', 'Title', 'Who', 'When', 'Video?', 'Slides?']
        c.data = []
        for t in talk_list:
            c.data.append(['<a href="/programme/schedule/view_talk/%d">%d</a>' % (t.id, t.id),
                           h.util.html_escape(t.title),
                           '<br/>'.join([
                                '<a href="/person/%d">%s</a> (<a href="mailto:%s">%s</a>)' % (
                                    p.id,
                                    h.util.html_escape(p.fullname),
                                    h.util.html_escape(p.email_address),
                                    h.util.html_escape(p.email_address)
                                ) for p in t.people
                           ]),
                           h.util.html_escape(t.scheduled),
                           h.util.html_escape(t.video_release),
                           h.util.html_escape(t.slides_release),
            ])
        c.noescape = True
        return table_response()

    @authorize(h.auth.has_organiser_role)
    def av_technical_requirements(self):
        """ Technical requirements list [AV] """
        talk_list = Proposal.find_all_accepted().filter(Proposal.technical_requirements > '').join(ProposalStatus).filter(ProposalStatus.name == 'Accepted').join(Event).join(Schedule).join(TimeSlot).order_by(TimeSlot.start_time)

        c.columns = ['Talk', 'Title', 'Who', 'Where', 'When', 'Requirements']
        c.data = []
        for t in talk_list:
            c.data.append(['<a href="/programme/schedule/view_talk/%d">%d</a>' % (t.id, t.id),
                           h.util.html_escape(t.title),
                           '<br/>'.join([
                                '<a href="/person/%d">%s</a> (<a href="mailto:%s">%s</a>)' % (
                                    p.id,
                                    h.util.html_escape(p.fullname),
                                    h.util.html_escape(p.email_address),
                                    h.util.html_escape(p.email_address)
                                ) for p in t.people
                           ]),
                           h.util.html_escape(h.list_to_string([schedule.location.display_name for schedule in t.event.schedule])),
                           h.util.html_escape(h.list_to_string([str(schedule.time_slot.start_time) + ' - ' + str(schedule.time_slot.end_time) for schedule in t.event.schedule])),
                           h.util.html_escape(t.technical_requirements),
            ])
        c.noescape = True
        return table_response()

    @authorize(h.auth.has_organiser_role)
    def random_delegates(self):
        """ Select 20 random (paid, non-volunteer, non-organiser, non-speaker, non-media) delegates for prize draws """

        filtered_list = []

        for r in Registration.find_all():
            p = r.person
            if p.is_speaker() or p.is_volunteer():
                continue
            if len(filter(lambda r: r.name in ('core_team', 'miniconfsonly', 'press', 'team', 'organiser', 'miniconf'), p.roles)):
                continue
            if p.paid() and p.has_paid_ticket():
                filtered_list.append(r)

        random.shuffle(filtered_list)

        c.columns = ['Who', 'From', 'Email', 'Shell', 'Nick', 'Twitter', 'Previous LCAs']
        c.data = []
        sn_twitter = SocialNetwork.find_by_name("Twitter")
        for r in filtered_list[:20]:
            c.data.append([
                "%s %s (%d)" % (r.person.firstname, r.person.lastname, r.person.id),
                "%s, %s" % (r.person.city, r.person.country),
                r.person.email_address,
                r.shell,
                r.nick,
                r.person.social_networks.get(sn_twitter),
                ','.join(r.prevlca or []),
            ])
        return table_response()

    @authorize(h.auth.has_organiser_role)
    def _destroy_personal_information(self):
        """ Remove personal information from the database (HIGHLY DESTRUCTIVE!) [Other] """
        return 'Disabled in controllers/admin.py. <br>Go enable it there if you really need it (i.e. LCA is well over and you have a <b>backup of the database</b>).<br><font color="#FF0000">You have been warned!</font>'
        people = Person().find_all()
        for person in people:
            # optional fields can be cleared
            person.company = '';
            person.address2 = '';
            person.state = '';
            person.phone = '';
            person.mobile = '';
            person.url = '';

            # required fields need some stuff in them
            person.address1 = 'deleted';
            person.city = 'deleted';
            person.postcode = 'deleted';
            person.country = 'AUSTRALIA';
            person.url = '';

            for sn in person.social_networks:
                person.social_networks[sn] = '';

        # Other tables which include personal information

        rego_notes = RegoNote().find_all()
        for note in rego_notes:
            meta.Session.delete(note)

        volunteers = Volunteer().find_all()
        for volunteer in volunteers:
            volunteer.other = ''
            volunteer.experience = ''

        special_regos = SpecialRegistration().find_all()
        for special in special_regos:
            meta.Session.delete(special)

        reviews = FundingReview().find_all()
        for review in reviews:
            meta.Session.delete(review)

        fundings = Funding().find_all()
        for funding in fundings:
            meta.Session.delete(funding)

        meta.Session.commit()
        return 'All done!'

    @authorize(h.auth.has_organiser_role)
    def lookup(self):
        """ Look up a person/rego, based on any of the associated IDs,
        showing the details as would be required for support or rego desk.
        [Registrations,Accounts,Invoicing] """

        # Start assuming we have a POST
        args = request.POST
        post=True

        # If we don't have a POST use GET instead
        if not args:
            args = request.GET
            post = False

        # If we have a person id find the person and return it
        if args.has_key('p'):
            try:
                person_id = int(args['p'])
            except:
                pass
            else:
                person = meta.Session.query(Person).get(person_id)
                if person:
                    c.id_type = 'Person ID'
                    c.person = person
                else:
                    c.error = 'Not found.'

        elif args.has_key('q'):
            query = args['q']
            c.query = args['q']
            results = []

            results += meta.Session.query(Person).filter(
                or_(
                    Person.email_address.ilike(query),
                    Person.email_address.ilike('%' + query + '%'),
                    Person.firstname.ilike(query),
                    Person.lastname.ilike(query),
                    Person.firstname.ilike('%' + query + '%'),
                    Person.lastname.ilike('%' + query + '%'),
                    Person.id.in_(meta.Session.query(Invoice.person_id).join(PaymentReceived).filter(PaymentReceived.gateway_ref == query))
                ),
            )

            try:
                query = int(args['q'])
            except:
                pass
            else:
                results += meta.Session.query(Person).filter(
                    or_(
                        Person.id == query,
                        Person.id.in_(meta.Session.query(Invoice.person_id).filter(Invoice.id == query)),
                        Person.id.in_(meta.Session.query(Registration.person_id).filter(Registration.id == query)),
                    )
                ).all()

            if len(results) == 1:
                c.person = results[0]

            elif len(results) > 1:
                kf = lambda r: ((r.lastname or 'ZZZ') + (r.firstname or 'ZZZ')).lower()
                cf = lambda f: lambda a,b: cmp(f(a), f(b))
                c.many = results
                c.many.sort(cf(kf))
            else:
                c.error = 'Not found.'
        else:
            c.error = 'Enter an ID or name in the box on right.'

        return render('admin/lookup.mako')

    def generate_fulfilment(self):
        """ Based on currently paid invoices, generate fulfilment records
            [Registration,Invoicing] """
        invoice_query = meta.Session.query(Invoice.person_id, InvoiceItem.product_id, Product.fulfilment_type_id, func.sum(InvoiceItem.qty).label('qty')).join(InvoiceItem).join(Product).filter(Product.fulfilment_type != None, Invoice.is_paid == True).group_by(Invoice.person_id, InvoiceItem.product_id, Product.fulfilment_type_id)
        fulfilment_query = meta.Session.query(Fulfilment.person_id, FulfilmentItem.product_id, Fulfilment.type_id, -func.sum(FulfilmentItem.qty).label('qty')).join(FulfilmentItem).join(FulfilmentStatus).filter(FulfilmentStatus.void == False).group_by(Fulfilment.person_id, FulfilmentItem.product_id, Fulfilment.type_id)
        union_query = invoice_query.union(fulfilment_query)
        columns = { d['name']: d['expr']  for d in union_query.column_descriptions }
        outstanding_query = union_query.with_entities(Person, Product, FulfilmentType, func.sum(columns['qty']).label('qty')).join(Person).join(Product).join(FulfilmentType, columns['fulfilment_type_id'] == FulfilmentType.id).group_by(Person, Product, FulfilmentType).having(func.sum(columns['qty']) != 0)
        outstanding = outstanding_query.all()

        for outstanding_item in outstanding:
            # Find existing FulfilmentGroup or generate a new one
            try:
                fulfilment_group = meta.Session.query(FulfilmentGroup).filter(FulfilmentGroup.person == outstanding_item.Person).one()
            except:
                code = generate_code(7, meta.Session.query(FulfilmentGroup.code))
                fulfilment_group = FulfilmentGroup(person=outstanding_item.Person, code=code)
                meta.Session.add(fulfilment_group)

            # Find the Fulfilment this item should belong to where it is still editable or create a new one
            try:
                fulfilment = meta.Session.query(Fulfilment).filter(Fulfilment.person == outstanding_item.Person, Fulfilment.type == outstanding_item.FulfilmentType, Fulfilment.can_edit == True).one()
            except:
                code = generate_code(5, meta.Session.query(Fulfilment.code))
                fulfilment = Fulfilment(person=outstanding_item.Person, type=outstanding_item.FulfilmentType, code=code)
                fulfilment_group.fulfilments.append(fulfilment)
                meta.Session.add(fulfilment)

            # Find fulfilment item record for this person/product. Make it part of the correct fulfilment and update the qty. Otherwise create a new one
            try:
                fulfilment_item = meta.Session.query(FulfilmentItem).join(Fulfilment).filter(Fulfilment.person == outstanding_item.Person, Fulfilment.type == outstanding_item.FulfilmentType, FulfilmentItem.product == outstanding_item.Product, Fulfilment.can_edit == True).one()
                fulfilment_item.fulfilment = fulfilment
                fulfilment_item.qty += outstanding_item.qty
                if fulfilment_item.qty == 0:
                    meta.Session.delete(fulfilment_item)
            except:
                fulfilment_item = FulfilmentItem(fulfilment=fulfilment, product=outstanding_item.Product, qty=outstanding_item.qty)
                meta.Session.add(fulfilment_item)

            meta.Session.commit()
        c.columns = ['Person', 'Product', 'FulfilmentType', 'Qty']
        c.data = [[result.Person.fullname, result.Product.category.name + ' - ' + result.Product.description, result.FulfilmentType.name, result.qty] for result in outstanding]
        return table_response()

    def fulfilment_report(self):
        return sql_response("""
                select description,
                       sum(completed) as completed,
                       sum(non_completed) as non_completed
                from (
                       select pc.name || ' => ' || p.description as description,
                             case when fs.name = 'Completed' then fi.qty else 0 end as completed,
                             case when fs.name <> 'Completed' then fi.qty else 0 end as non_completed
                      from fulfilment f,
                            fulfilment_item fi,
                            product p,
                            product_category pc,
                            fulfilment_status fs
                       where fi.fulfilment_id = f.id
                         and fi.product_id = p.id
                         and pc.id = p.category_id
                         and f.status_id = fs.id
                         and not fs.void
                     ) data
                group by description
                order by description
            """)
    def generate_boardingpass(self):
        """ For every fulfilment group, generate a boarding pass
            [Registration,Invoicing] """
        from zkpylons.lib import pdfgen
        from zkpylons.config.zkpylons_config import file_paths
        groups = FulfilmentGroup.find_all()
        for group in groups:
            c.fulfilment_group = group

            xml_s = render('/fulfilment_group/pdf.mako')
            xsl_f = app_globals.mako_lookup.get_template('/fulfilment_group/pdf.xsl').filename
            pdf_data = pdfgen.generate_pdf(xml_s, xsl_f)

            if c.fulfilment_group.person:
                filename = c.fulfilment_group.person.email_address + '.pdf'
            else:
                filename = lca_info['event_shortname'] + '_' + str(c.fulfilment_group.id) + '.pdf'
            pdf = open(file_paths['zk_root'] + '/boardingpass/' + filename, 'w')
            pdf.write(pdf_data)
            pdf.close()
        return "Completed"

    def generate_fulfilment_codes(self):
        for fulfilment in meta.Session.query(Fulfilment).all():
            if not fulfilment.code:
                fulfilment.code = generate_code(5, meta.Session.query(Fulfilment.code))
        meta.Session.commit()
        return 'Completed'

def generate_code(length=7, selectable=None):
    while True:
        res = os.popen('pwgen ' + str(length) + ' -BnA').read().strip()
        if len(res)<length:
            raise StandardError("pwgen call failed")
        if selectable and res not in [row[0] for row in selectable.all()]:
            break
    return res

def _keysigning_pdf(keyid):
    import os, tempfile, subprocess
    max_length = 66
    (txt_fd, txt) = tempfile.mkstemp('.txt')
    (pdf_fd, pdf) = tempfile.mkstemp('.pdf')
    os.system('gpg --recv-keys --keyserver keys.keysigning.org ' + keyid)
    fingerprint = subprocess.Popen(['gpg', '--fingerprint', keyid], stdout=subprocess.PIPE).communicate()[0]
    fingerprint_length = len(fingerprint.splitlines())
    if fingerprint_length > 0:
        fingerprint_num = max_length / int(fingerprint_length)
    else:
        fingerprint_num = 0
    for i in range(0,fingerprint_num):
        os.system('gpg --fingerprint %s >> %s' % (keyid, txt))
    os.system('mpage -1 -W `wc -L < %s` %s | ps2pdf - %s' % (txt, txt, pdf))
    os.close(pdf_fd);
    os.close(txt_fd);

    return pdf

def csv_response(sql):
    res = meta.Session.execute(sql)
    c.columns = get_column_names(res)
    c.data = res.fetchall()
    c.sql = sql

    # Convert to utf-8 so that csv writer can handle the strings
    c.data = [[unicode(s).encode("utf-8") for s in row] for row in c.data]

    import csv, StringIO
    f = StringIO.StringIO()
    w = csv.writer(f)
    w.writerow(c.columns)
    w.writerows(c.data)
    response.headers['Content-type']='text/plain; charset=utf-8'
    response.headers['Content-Disposition']='attachment; filename="table.csv"'
    return f.getvalue()

#
# Something changed between sqlalchmey 0.5.7 and 0.6.4.  ResultProxy.keys
# was a list, in 0.6.3 it is a function that returns the same list.
#
def get_column_names(result_proxy):
    try:
        return list(result_proxy.keys)
    except TypeError:
        return result_proxy.keys()

def sql_execute(sql):
    import zkpylons.model
    res = zkpylons.model.metadata.bind.execute(sql)
    return res

def sql_response(sql):
    """ This function bypasses all the MVC stuff and just puts up a table
    of results from the given SQL statement.

    Ideally, of course, it should never be used.

    Example:
        def foo(self):
            return sql_response('select * from person')
    """
    if request.GET.has_key('csv'):
        return csv_response(sql)
    res = meta.Session.execute(sql)
    c.columns = get_column_names(res)
    if hasattr(c.columns, "__call__"):        # work around for bug in sqlalchemy 0.5.7
      c.columns = c.columns()
    c.data = res.fetchall()
    c.sql = sql
    return render('admin/sqltable.mako')

def sql_data(sql):
    """ This function bypasses all the MVC stuff and just gives you a
    two-dimensional array based on the given SQL statement.

    Ideally, of course, it should never be used.
    """
    import zkpylons.model
    return zkpylons.model.metadata.bind.execute(sql).fetchall();

def table_response():
    """ Display a table of data, possible jumping off to CSV. """
    if request.GET.has_key('csv'):
        return table_csv_response()
    elif request.GET.has_key('latex'):
      response.headers['Content-type']='text/plain; charset=utf-8'
      response.headers['Content-Disposition']='attachment; filename="table.tex"'

      return render('admin/table_latex.mako')

    return render('admin/table.mako')

def table_csv_response():
    import csv, StringIO
    f = StringIO.StringIO()
    w = csv.writer(f)
    w.writerow(c.columns)
    w.writerows(c.data)
    response.headers['Content-type']='text/plain; charset=utf-8'
    response.headers['Content-Disposition']='attachment; filename="table.csv"'
    return f.getvalue()
