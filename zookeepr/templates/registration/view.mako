<%inherit file="/base.mako" />

        <h2>Your registration details</h2>
        <p>Here are the registration details we have for you.</p>
        <p>${ h.link_to('Registration status', url=h.url_for(action='status')) }</p>

        <h2>About yourself</h2>

        <p class="label">Your first name:</p>
        <p>${ c.registration.person.firstname | h }</p>

        <p class="label">Your last name:</p>
        <p>${ c.registration.person.lastname | h }</p>

        <p class="label">Email address:</p>
        <p>${ c.registration.person.email_address | h }</p>
        <p class="note">Your email address will only be used to correspond with you, and is your login name for the website.  It will not be shown or used otherwise.</p>

        <h2>Personal Information</h2>

        <p class="label">Address:</p>
        <p>
          ${ c.registration.person.address1 | h }
          <br>
          ${ c.registration.person.address2 | h }
        </p>
        <p class="label">City/Suburb:</p>
        <p>${ c.registration.person.city | h }</p>
        <p class="label">State/Province:</p>
        <p>${ c.registration.person.state | h }</p>
        <p class="label">Country:</p>
        <p>${ c.registration.person.country | h }</p>
        <p class="label">Postcode/ZIP:</p>
        <p>${ c.registration.person.postcode | h }</p>

        <p class="label">Phone number:</p>
        <p>${ c.registration.person.phone | h }</p>

        <p class="label">Mobile/Cell number:</p>
        <p>${ c.registration.person.mobile | h }</p>

        <p class="label">Company:</p>
        <p>${ c.registration.person.company | h }</p>

% for category in c.product_categories:

        <h2>${ category.name.title() }</h2>
%   for product in category.products:
%       for rproduct in c.registration.products:
%           if rproduct.product == product:
%               if category.display == 'qty':
        <p>${ rproduct.qty } x ${ product.description } - ${ h.number_to_currency(product.cost/100.0) }</p>
%               else:
        <p>${ product.description } - ${ h.number_to_currency(product.cost/100.0) }</p>
%               endif
%           endif
%       endfor
%   endfor
%   if category.name == 'Accommodation' and not h.lca_rego['accommodation']['self_book'] == 'yes':

        <p class="label">Check in on:</p>
        <p>${ h.date(c.registration.checkin) }</p>

        <p class="label">Check out on:</p>
        <p>${ h.date(c.registration.checkout) }</p>
%   elif category.name == 'Partners Programme':

        <p class="label">Your partner's email address:</p>
        <p>${ c.registration.partner_email | h }</p>
%   endif
% endfor

        <h2>Further Information</h2>

        <p>${ h.yesno(c.registration.over18) |n } Are you over 18?</p>

        <p class="label">Voucher Code:</p>
        <p>${ c.registration.voucher_code | h }</p>

        <p class="label">Dietary requirements:</p>
        <p>${ c.registration.diet | h }</p>

        <p class="label">Other special requirements:</p>
        <p>${ c.registration.special | h }</p>

        <p class="label">Preferred mini-confs:</p>
        <p>
          <table>
            <tr>
% for day, miniconfs in h.lca_rego['miniconfs']:
              <th>${ day }</th>
% endfor
            </tr>
            <tr>
% for day, miniconfs in h.lca_rego['miniconfs']:
              <td>
%   for miniconf in miniconfs:
<%       l = '%s_%s' % (day,miniconf.replace(' ', '_').replace('.', '_')) %>
                ${ h.yesno(l in (c.registration.miniconf or [])) |n }
                ${ miniconf }
                <br>
%   endfor
              </td>
% endfor
            </tr>
          </table>
          <p class="note">Please check the ${ h.link_to('mini-confs', url="/programme/mini-confs") } page for details on each event. You can choose to attend multiple mini-confs in the one day, as the schedules will be published ahead of the conference for you to swap sessions.</p>

          <p class="label"><label for="registration.prevlca">Have you attended linux.conf.au before?</label></p>
          <p class="entries">
% for (year, desc) in h.lca_rego['past_confs']:
            <br>
            ${ h.yesno(year in (c.registration.prevlca or [])) |n }
            ${ desc }
% endfor
          </p>

          <h2>Optional</h2>
          <p class="label">Your favourite shell:</p>
          <p>${ c.registration.shell | h }

          <p class="label">Your favourite editor:</p>
          <p>${ c.registration.editor | h }

          <p class="label">Your favourite distro:</p>
          <p>${ c.registration.distro | h }

          <p class="label">Superhero name:</p>
          <p>${ c.registration.nick | h }
          <p class="note">Your IRC nick or other handle you go by.</p>

          <p class="label">GnuPG/PGP Keyid:</p>
          <p>${ c.registration.keyid | h }

          <p class="label">Planet Feed:</p>
          <p>${ c.registration.planetfeed }</p>

          <p class="label"><label for="registration.silly_description">Description:</label></p>
          <blockquote><p>${ c.registration.silly_description | h }</p></blockquote>
          <p class="note">This is a randomly chosen description for your name badge</p>


          <h2>Subscriptions</h2>

          <p>${ h.yesno('linuxaustralia' in c.registration.signup) |n } I want to sign up for (free) Linux Australia membership!</p>

          <p>${ h.yesno('nzoss' in c.registration.signup) |n } I want to sign up for membership with the New Zealand Open Source Society.</p>

          <p>${ h.yesno('internetnz' in c.registration.signup) |n } I want to sign up for membership with the Internet NZ.</p>

          <p>${ h.yesno('announce' in c.registration.signup) |n } I want to sign up to the low traffic conference announcement mailing list!</p>

          <p>${ h.yesno('chat' in c.registration.signup) |n } I want to sign up to the conference attendees mailing list!</p>

% if c.registration.person.is_speaker():
          <h2>Speaker recording consent and release</h2>
          <p>As a service to Linux Australia members and to other interested Linux users,
          Linux Australia would like to make your presentation available to the public.
          This involves video­taping your talk, and offering the video/audio and slides
          (for download, or on CD­ROM).</p>

% endif

          <p>${ h.link_to('Edit details', h.url_for(action='edit', id=c.registration.id)) } - ${ h.link_to('back', url=h.url_for(action='status', id=None)) }<br>
