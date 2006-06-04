<div class="sidebarbox">
<div class="contentboxR">
<div class="contentboxC" id="sidebarboxTL"></div>
<div class="contentboxC" id="sidebarboxTR"></div>
</div>

<div class="sidebarcontent">

<%python>
if r.environ.has_key('REMOTE_USER'):
	from sqlalchemy import create_session
	from zookeepr.models import Person
	
	session = create_session()
	users = session.query(Person).select_by(email_address=r.environ['REMOTE_USER'])
	user = users[0]

	if user.handle is not None:
		id = user.handle
		display = user.handle
	else:
		id = user.id
		display = user.email_address

	m.write("logged in as ")
	m.write(h.link_to(display, url=h.url(controller='person', action='view', id=id)))
	m.write(". ")
	m.write(h.link_to('sign out', url=h.url(controller='/account', action='signout')))
</%python>


<ul>
<li><% h.link_to('Sign up', url=h.url(controller='person', action='new')) %></li>
<li><% h.link_to('Call for Participation', h.url(controller='about', action='view', id='cfp')) %></li>
<li><% h.link_to('Submit a proposal', h.url(controller='submission', action='new')) %></li>
</ul>
</div>

<div class="contentboxR" id="sidebarboxB">
<div class="contentboxC" id="sidebarboxBL"></div>
<div class="contentboxC" id="sidebarboxBR"></div>
</div>
</div>
