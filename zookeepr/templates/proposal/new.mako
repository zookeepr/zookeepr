<%inherit file="/base.mako" />

<h2>Propose a talk or tutorial</h2>
<p>Please read the <a href="${ h.url_for("/programme/presenter_faq") }">Presenter FAQ</a> before submitting a proposal.</p>

${ h.form(h.url_for(), multipart=True) }
<%include file="form.mako" />

  <p class="submit">${ h.submit('submit', 'Submit!') }</p>
${ h.end_form() }

<%def name="title()" >
Call for Presentations - ${ caller.title() }
</%def>


##${init>
### Working around a bug in formencode, we need to set the defaults to the c.proposal
### values
##if not defaults:
##    defaults = {
##        'proposal.type': 1,
##        'proposal.assistance': 4,
##    }
##    if c.signed_in_person:
##        c.person = c.signed_in_person
##        defaults['person.mobile'] = c.person.mobile
##        defaults['person.experience'] = c.person.experience
##        defaults['person.bio'] = c.person.bio
##</%init>
