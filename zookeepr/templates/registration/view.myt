        <h2>Your registration details</h2>
        <p>Here are the registration details we have for you.</p>
        <p><a href="/registration/status">Registration status</a></p>

        <h2>About yourself</h2>

        <p class="label">Your first name:</p>
        <p><% c.signed_in_person.firstname | h %></p>

        <p class="lavel">Your last name:</p>
        <p><% c.signed_in_person.lastname | h %></p>

        <p class="label">Email address:</p>
        <p><% c.signed_in_person.email_address | h %></p>
        <p class="note">Your email address will only be used to correspond with you, and is your login name for the website.  It will not be shown or used otherwise.</p>

        <h2>Personal Information</h2>

        <p class="label">Address:</p>
        <p>
          <% c.registration.person.address1 %>
          <br>
          <% c.registration.person.address2 %>
        </p>
        <p class="label">City/Suburb:</p>
        <p><% c.registration.person.city %></p>
        <p class="label">State/Province:</p>
        <p><% c.registration.person.state %></p>
        <p class="label">Country:</p>
        <p><% c.registration.person.country %></p>
        <p class="label">Postcode/ZIP:</p>
        <p><% c.registration.person.postcode %></p>

        <p class="label">Phone number:</p>
        <p><% c.registration.person.phone %></p>

        <p class="label">Mobile/Cell number:</p>
        <p><% c.registration.person.mobile %></p>

        <p class="label">Company:</p>
        <p><% c.registration.person.company %></p>

% for category in c.product_categories:

        <h2><% category.name.title() %></h2>
%   for product in category.products:
%       for rproduct in c.registration.products:
%           if rproduct.product == product:
%               if category.display == 'qty':
        <p><% rproduct.qty %> x <% product.description %> - $<% product.cost %></p>
%               else:
        <p><% product.description %> - $<% product.cost %></p>
%               #endif
%           #endif
%       #endfor
%   #endfor
%   if category.name == 'Accomodation':

        <p class="label">Check in on:</p>
        <p><% date(c.registration.checkin) %></p>

        <p class="label">Check out on:</p>
        <p><% date(c.registration.checkout) %></p>
%   elif category.name == 'Partners Programme':

        <p class="label">Your partner's email address:</p>
        <p><% c.registration.partner_email %></p>
%   #endif
% #endfor

        <h2>Further Information</h2>

        <p class="label">Dietary requirements:</p>
        <p><% c.registration.diet %></p>

        <p class="label">Other special requirements:</p>
        <p><% c.registration.special %></p>

        <p class="label">Preferred mini-confs:</p>
        <p>
          <table>
            <tr>
% for day, miniconfs in h.lca_rego['miniconfs']:
              <th><% day %></th>
% #endfor
            </tr>
            <tr>
% for day, miniconfs in h.lca_rego['miniconfs']:
              <td>
%   for miniconf in miniconfs:
%       l = '%s' % miniconf.replace(' ', '_').replace('.', '_')
                <% yesno(l in (c.registration.miniconf or [])) %>
                <% miniconf %>
                <br>
%   #endfor
              </td>
% #endfor
            </tr>
          </table>
          <p class="note">Please check the <% h.link_to('mini-confs', url="/programme/mini-confs") %> page for details on each event. You can choose to attend multiple mini-confs in the one day, as the schedules will be published ahead of the conference for you to swap sessions.</p>

          <p class="label">How many people are you bringing to Open Day?</p>
          <p><% c.registration.opendaydrag %></p>
          <p class="note">Open Day is open to friends and family, and is targeted to a non-technical audience.  If you want to show off FOSS culture to some people, you can give us an idea of how many people to expect.</p>

          <p class="label">Your favourite shell:</p>
          <p><% c.registration.shell %>

          <p class="label">Your favourite editor:</p>
          <p><% c.registration.editor %>

          <p class="label">Your favourite distro:</p>
          <p><% c.registration.distro %>

          <p class="label">Superhero name:</p>
          <p><% c.registration.nick %>
          <p class="note">Your IRC nick or other handle you go by.</p>

          <p class="label"><label for="registration.prevlca">Have you attended linux.conf.au before?</label></p>
          <p class="entries">
% for (year, desc) in h.lca_rego['past_confs']:
            <br>
            <% yesno(year in (c.registration.prevlca or [])) %>
            <% desc %>
% #endfor
          </p>

          <p class="label"><label for="registration.silly_description">Description:</label></p>
          <blockquote><p><% c.registration.silly_description %></p></blockquote>
          <p class="note">This is a randomly chosen description for your name badge</p>

          <h2>Subscriptions</h2>

          <p><% yesno(c.registration.lasignup) %> I want to sign up for (free) Linux Australia membership!</p>

          <p><% yesno(c.registration.announcesignup) %> I want to sign up to the low traffic conference announcement mailing list!</p>

          <p><% yesno(c.registration.delegatesignup) %> I want to sign up to the conference attendees mailing list!</p>

% if c.registration.person.is_speaker():
          <h2>Speaker recording consent and release</h2>
          <p>As a service to Linux Australia members and to other interested Linux users,
          Linux Australia would like to make your presentation available to the public.
          This involves video­taping your talk, and offering the video/audio and slides
          (for download, or on CD­ROM).</p>

          <p><% yesno(c.registration.speaker_record) %> I allow Linux Australia to record my presentation</p>

          <p><% yesno(c.registration.speaker_video_release) %> I allow Linux Australia to release my video under the Creative Commons ShareAlike License</p>

          <p><% yesno(c.registration.speaker_slides_release) %> I allow Linux Australia to share my slides</p>

          <p>If you have allowed Linux Australia to publish your slides, there will
          be an upload mechanism closer to the conference. We will publish them under
          the Creative Commons Attribution License unless you have an equivalent
          preference that you let us know.</p>
% #endif
<%init>
def yesno(bool):
    if bool:
        return '&#9745'
    else:
        return '&#9744'
def num(x):
    if x==None:
        return 'none'
    else:
        return x
def date(d):
    if d==1:
        return "%dst of January" % d
    elif d==2:
        return "%dnd of January" % d
    elif d==3:
        return "%drd of January" % d
    elif d<15:
        return "%dth of January" % d
    elif d==31:
        return "%dst of January" % d
    else:
        return "%dth of January" % d

</%init>
