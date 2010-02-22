<%inherit file="/base.mako" />

        <h2>Your registration details</h2>
        <p>Here are the registration details we have for you.</p>

        <blockquote>
        <p>
        ${ c.registration.person.firstname } ${ c.registration.person.lastname }
        <br/>${ c.registration.person.address1 }
%if c.registration.person.address2:
        <br/>${ c.registration.person.address2 }
%endif
%if c.registration.person.state:
        <br/>${ c.registration.person.city }
        <br/>${ c.registration.person.state }, ${ c.registration.person.postcode }
%else:
        <br/>${ c.registration.person.city }, ${ c.registration.person.postcode }
%endif
        <br/>${ c.registration.person.country }
        </p>
        </blockquote>
%if c.registration.person.phone:
        <p class="label"><b>Phone number:</b> ${ c.registration.person.phone }</p>
%endif
%if c.registration.person.mobile:
        <p class="label"><b>Mobile/Cell number:</b> ${ c.registration.person.mobile }</p>
%endif
%if c.registration.person.company:
        <p class="label"><b>Company:</b> ${ c.registration.person.company }</p>
%endif

% for category in c.product_categories:

<%  category_printed = False %>

%if category.name != 'Accommodation' or h.lca_rego['accommodation']['self_book'] != 'yes':

%   for product in category.products:
%       for rproduct in c.registration.products:
%           if rproduct.product == product:
%               if not category_printed:
        <h2>${ category.name.title() }</h2>
<%                category_printed = True %>
%               endif
%               if category.display == 'qty':
        <p>${ rproduct.qty } x ${ product.description } - ${ h.number_to_currency(product.cost/100.0) }</p>
%               else:
        <p>${ product.description } - ${ h.number_to_currency(product.cost/100.0) }</p>
%               endif
%           endif
%       endfor
%   endfor
%   if category.name == 'Accommodation':

        <p class="label">Check in on:</p>
        <p>${ h.date(c.registration.checkin) }</p>

        <p class="label">Check out on:</p>
        <p>${ h.date(c.registration.checkout) }</p>
%   elif category.name == 'Partners Programme':
%     if c.registration.partner_name:
        <p class="label"><b>Your partner's name:</b> ${ c.registration.partner_name }</p>
%     endif
%     if c.registration.partner_email:
        <p class="label"><b>Your partner's email address:</b> ${ c.registration.partner_email }</p>
%     endif
%     if c.registration.partner_mobile:
        <p class="label"><b>Your partner's mobile number:</b> ${ c.registration.partner_mobile }</p>
%     endif
%   endif
%endif
% endfor

        <h2>Further Information</h2>

        <p>${ h.yesno(c.registration.over18) |n } Over 18 year old</p>

%if c.registration.voucher_code:
        <p class="label"><b>Voucher Code:</b> ${ c.registration.voucher_code }</p>
%endif
%if c.registration.diet:
        <p class="label"><b>Dietary requirements:</b> ${ c.registration.diet }</p>
%endif
%if c.registration.special:
        <p class="label"><b>Other special requirements:</b> ${ c.registration.special }</p>
%endif
        <p class="label"><b>Preferred mini-confs:</b></p>
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

          <p class="label"><label for="registration.prevlca"><b>Previous LCA attendance:</b></label></p>
          <p class="entries">
% for (year, desc) in h.lca_rego['past_confs']:
            <br>
            ${ h.yesno(year in (c.registration.prevlca or [])) |n }
            ${ desc }
% endfor
          </p>

%if c.registration.shell:
          <p class="label"><b>Your favourite shell:</b> ${ c.registration.shell }</p>
%endif
%if c.registration.editor:
          <p class="label"><b>Your favourite editor:</b> ${ c.registration.editor }</p>
%endif
%if c.registration.distro:
          <p class="label"><b>Your favourite distro:</b> ${ c.registration.distro }</p>
%endif
%if c.registration.nick:
          <p class="label"><b>Superhero name:</b> ${ c.registration.nick }</p>
%endif
%if h.lca_rego['pgp_collection'] != 'no' and c.registration.keyid:
          <p class="label"><b>GnuPG/PGP Keyid:</b> ${ c.registration.keyid }</p>
%endif
%if c.registration.planetfeed:
          <p class="label"><b>Planet Feed:</b> ${ c.registration.planetfeed }</p>
%endif
          <p class="label"><label for="registration.silly_description"><b>Description:</b> ${ c.registration.silly_description }</p>
          <p class="note">This is a randomly chosen description for your name badge</p>

          <h2>Subscriptions</h2>

          <p>${ h.yesno('linuxaustralia' in (c.registration.signup or [])) |n } I want to sign up for (free) Linux Australia membership!</p>

          <p>${ h.yesno('nzoss' in (c.registration.signup or [])) |n } I want to sign up for membership with the New Zealand Open Source Society.</p>

          <p>${ h.yesno('internetnz' in (c.registration.signup or [])) |n } I want to sign up for membership with the Internet NZ.</p>

          <p>${ h.yesno('announce' in (c.registration.signup or [])) |n } I want to sign up to the low traffic conference announcement mailing list!</p>

          <p>${ h.yesno('chat' in (c.registration.signup or [])) |n } I want to sign up to the conference attendees mailing list!</p>

% if c.registration.person.is_speaker():
          <h2>Speaker recording consent and release</h2>
          <p>As a service to Linux Australia members and to other interested Linux users,
          Linux Australia would like to make your presentation available to the public.
          This involves video­taping your talk, and offering the video/audio and slides
          (for download, or on CD­ROM).</p>

% endif

          <p>${ h.link_to('Edit details', h.url_for(action='edit', id=c.registration.id)) } - ${ h.link_to('back', url=h.url_for(action='status', id=None)) }<br>
