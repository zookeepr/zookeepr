<%
import datetime
%>
        <fieldset id="person">
          <legend>&nbsp;</legend>
          <h2>About yourself</h2>

% if not h.signed_in_person():
          <p class="note"><span class="mandatory">*</span> - Mandatory field</p>
% endif
          <p class="label">
% if not c.signed_in_person:
            <span class="mandatory">*</span>
% endif
            <label for="person.firstname">Your first name:</label>
          </p>
% if c.registration and c.registration.person:
          <p>${ c.registration.person.firstname | h }</p>
% elif c.signed_in_person:
          <p>${ c.signed_in_person.firstname | h }</p>
% else:
          <p class="entries">${ h.text('person.firstname', size=40) }</p>
% endif

          <p class="label">
% if not c.signed_in_person:
            <span class="mandatory">*</span>
% endif
            <label for="person.lastname">Your last name:</label>
          </p>
% if c.registration and c.registration.person:
          <p>${ c.registration.person.lastname | h }</p>
% elif c.signed_in_person:
          <p>${ c.signed_in_person.lastname | h }</p>
% else:
          <p class="entries">${ h.text('person.lastname', size=40) }</p>
% endif

          <p class="label">
% if not c.signed_in_person:
            <span class="mandatory">*</span>
% endif
            <label for="person.email_address">Email address:</label>
          </p>
% if c.registration and c.registration.person:
          <p>${ c.registration.person.email_address | h }</p>
% elif c.signed_in_person:
          <p>${ c.signed_in_person.email_address | h }</p>
% else:
          <p class="entries">${ h.text('person.email_address', size=40) }</p>
% endif
          <p class="note">Your email address will only be used to correspond with you, and is your login name for the website.  It will not be shown or used otherwise.</p>
% if not c.signed_in_person:

          <p class="label"><span class="mandatory">*</span><label for="person.password">Choose a password:</label></p>
          <p class="entries">${ h.password("person.password", size=40) }</p>

          <p class="label"><span class="mandatory">*</span><label for="person.password_confirm">Confirm your password:</label></p>
          <p class="entries">${ h.password("person.password_confirm", size=40) }</p>
% endif
        </fieldset>

        <fieldset id="personal">
          <legend>&nbsp;</legend>
          <h2>Personal Information</h2>

          <p class="note"><span class="mandatory">*</span> - Mandatory field</p>

          <p class="label"><span class="mandatory">*</span><label for="person.address">Address:</label></p>
          <p class="entries">
            ${ h.text('person.address1', size=40) }
            <br>
            ${ h.text('person.address2', size=40) }
          </p>

          <p class="label"><span class="mandatory">*</span><label for="person.city">City/Suburb:</label></p>
          <p class="entries">${ h.text('person.city', size=40) }</p>

          <p class="label"><label for="person.state">State/Province:</label></p>
          <p class="entries">${ h.text('person.state', size=40) }</p>

          <p class="label"><span class="mandatory">*</span><label for="person.country">Country:</label></p>
          <p class="entries">
            <select name="person.country">
% for country in h.countries():
              <option value="${country}">${ country }</option>
% endfor
            </select>
          </p>

          <p class="label"><span class="mandatory">*</span><label for="person.postcode">Postcode/ZIP:</label></p>
          <p class="entries">${ h.text('person.postcode', size=40) }</p>

<%
if h.signed_in_person():
  is_speaker = c.signed_in_person.is_speaker()
else:
  is_speaker = False
%>

          <p class="label"><label for="person.mobile">Phone number:</label></p>
          <p class="entries">${ h.text('person.phone') }</p>

          <p class="label">
% if is_speaker:
            <span class="mandatory">*</span>
% endif
            <label for="person.mobile">Mobile/Cell number:</label>
          </p>
          <p class="entries">${ h.text('person.mobile') }</p>

          <p class="label"><label for="person.company">Company:</label></p>
          <p class="entries">${ h.text('person.company', size=60) }</p>

        </fieldset>
% for category in c.product_categories:
<%
  all_products = category.available_products(c.signed_in_person, stock=False)
  products = []
  for product in all_products:
      if c.product_available(product, stock=False):
          products.append(product)
%>
%   if len(products) > 0:

        <fieldset id="${ h.computer_title(category.name) }">
          <legend>&nbsp;</legend>
          <h2>${ category.name.title() }</h2>
          <p class="note">${ category.description }</p>
## Manual category display goes here:
%       if category.name == 'Shirt':
<%
##         # fields need to be exactly the same order as the shirts in the DB, this just replaces their name.
##         # Number of items in the row must be the same for each row
           fields = [("Men's Short Sleeved Shirt", ['S', 'M', 'L', 'XL', 'XXL', 'XXXL', 'XXXXL', 'XXXXXL']),("Women's Short Sleeved Shirt", ['S', 'M', 'L', 'XL', 'XXL', 'XXXL', 'XXXXL', 'XXXXXL'])]
           i = j = 0
%>
          <p>S,M,L,XL shirts are $20 each, larger shirts are $22. More details and measurements on shirt sizes can be found on the ${ h.link_to('registration information', url='/register/shirts', popup=True) }.</p>
          <table>
            <tr><th><span class="mandatory">*</span>Please pick at least one</th><th>S</th><th>M</th><th>L</th><th>XL</th><th>XXL</th><th>XXXL</th><th>XXXXL</th><th>XXXXXL</th></tr>
            <tr><td>${ fields[0][0] }</td>
%           for product in products:
%               if j == len(fields[i][1]):
<%
                   i += 1
                   j = 0
%>
            </tr><tr><td>${ fields[i][0] }</td>
%               endif
%               if not product.available():
            <td><span class="mandatory">^</span>${ h.text('none', size=2, disabled=True) }${ h.hidden_field('products.product_' + str(product.id) + '_qty') }</td>
%               else:
            <td>${ h.text('products.product_' + str(product.id) + '_qty', size=2) }</td>
%               endif
             <% j += 1 %>
%           endfor
          </tr></table><p><span class="mandatory">^</span>Sold out</p>
%       elif category.display == 'radio':
%           for product in products:
<%
               soldout = ''
               if not product.available():
                   soldout = ' <span class="mandatory">SOLD OUT</span> '
%>
          <p><label>${ h.radio('products.category_' + str(category.id), product.id) }${ soldout }${ product.description } - ${ h.number_to_currency(product.cost/100.0) }</label></p>
%           endfor
%       elif category.display == 'select':
          <p class="entries">
            <select name="products.category_${ category.id }">
              <option value=""> - </option>
%           for product in products:
<%
               soldout = ''
               if not product.available():
                   soldout = ' SOLD OUT '
               endif
%>
              <option value="${ product.id }"> ${ soldout }${ product.description } - ${ h.number_to_currency(product.cost/100.0) }</option>
%           endfor
            </select>
          </p>
%       elif category.display == 'checkbox':
%           for product in products:
<%
               soldout = ''
               if not product.available():
                   soldout = ' <span class="mandatory">SOLD OUT</span> '
%>
          <p><label>${ h.checkbox('products.product_' + str(product.id)) }${ soldout }${ product.description } - ${ h.number_to_currency(product.cost/100.0) }</label></p>
%           endfor
%       elif category.display == 'qty':
%           for product in products:
<%
               soldout = ''
               if not product.available():
                   soldout = ' <span class="mandatory">SOLD OUT</span> '
%>
          <p>${ soldout }${ product.description } ${ h.text('products.product_' + str(product.id) + '_qty', size=2) } x ${ h.number_to_currency(product.cost/100.0) }</p>
%           endfor
%       endif
%       if category.name == 'Accommodation':
          <p>Please see ${ h.link_to('the accommodation page', url='/register/accommodation', popup=True) } for prices and details, including how to book your Wrest Point room at LCA09 rates.</p>
          <p class="label"><span class="mandatory">*</span><label for="registration.checkin">Check in on:</label></p>
          <p class="entries">
            <select name="registration.checkin">
         <% dates = [(d, 1) for d in range(17,25)] %>
%           for (day, month) in dates[:-1]:
              <option value="${ day }">${ datetime.datetime(2010, month, day).strftime('%A, %e %b') }</option>
%           endfor
            </select>
          </p>

          <p class="label"><span class="mandatory">*</span><label for="registation.checkout">Check out on:</label></p>
          <p class="entries">
            <select name="registration.checkout">
%           for (day, month) in dates[1:]:
              <option value="${ day }" >${ datetime.datetime(2010, month, day).strftime('%A, %e %b') }</option>
%           endfor
            </select>
          </p>
%       elif category.name == 'Partners Programme':
          <p class="label"><span class="mandatory">^</span><label for="registration.partner_email">Your partner's email address:</label></p>
          <p class="entries">${ h.text('products.partner_email', size=50) }</p>
          <p class="note">^If your partner will be participating in the programme, then this field is required so that our Partners Programme manager can contact them.</p>
          <p class="note">A partners programme shirt is included with each partner ticket. We will email the above address to get shirt sizes before the conference.</p>
%       endif
        </fieldset>
%   endif
% endfor

        <fieldset>
          <legend>&nbsp;</legend>
          <h2>Further Information</h2>

          <p class="entries">${ h.checkbox('registration.over18') }<label for="registrationover18">Are you over 18?</label></p>
          <p class="note">Being under 18 will not stop you from registering. We need to know whether you are over 18 to allow us to cater for you at venues that serve alcohol.</p>

          <p class="label"><label for="registration.voucher_code">Voucher Code</label></p>
          <p class="entries">${ h.text('registration.voucher_code', size=15) }</p>
          <p class="note">If you have been provided with a voucher code enter it here.</p>

          <p class="label"><label for="registration.diet">Dietary requirements:</label></p>
          <p class="entries">${ h.text('registration.diet', size=60) }</p>

          <p class="label"><label for="registration.special">Other special requirements</label></p>
          <p class="entries">${ h.text('registration.special', size=60) }</p>
          <p class="note">Please enter any requirements if necessary; access requirements, etc.</p>

          <p class="label"><label for="registration.miniconfs">Preferred mini-confs:</label></p>
          <p class="entries">
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
        <% label = 'registration.miniconf.%s_%s' % (day,miniconf.replace(' ', '_').replace('.', '_')) %>
                  ${ h.checkbox(label) }
                  <label for="${ label }">${ miniconf }</label>
                  <br>
%   endfor
                </td>
% endfor
              </tr>
            </table>

            <p class="note">Please check the ${ h.link_to('miniconfs', url="/programme/miniconfs", popup=True) } page for details on each event. You can choose to attend multiple miniconfs in the one day, as the schedules will be published ahead of the conference for you to swap sessions.</p>

            <p class="label"><label for="registration.prevlca">Have you attended linux.conf.au before?</label></p>
            <p class="entries">
% for (year, desc) in h.lca_rego['past_confs']:
   <% label = 'registration.prevlca.%s' % year %>
                ${ h.checkbox(label) }
                <label for="${ label }">${ desc }</label>
                <br>
% endfor
            </p>
          </fieldset>

          <fieldset>
            <legend>&nbsp;</legend>
            <h2>Optional</h2>
<table>
<tr>
  <td>
            <p class="label"><label for="registration.shell">Your favourite shell:</label></p>
            <p class="entries">
              <select id="registration.shell" name="registration.shell" onchange="toggle_select_hidden(this.id, 'shell_other')">
                <option value="">(please select)</option>
% for s in h.lca_rego['shells']:
                <option value="${s}">${ s }</option>
% endfor
                <option value="other">other:</option>
              </select>
% if not registration or registration.shell in h.lca_rego['shells'] or registration.shell == '':
              <span id="shell_other" style="display: none">${ h.text('registration.shelltext') }</span>
% else:
              <span id="shell_other" style="display: inline">${ h.text('registration.shelltext') }</span>
% endif
            </p>
  </td>
  <td>

            <p class="label"><label for="registration.editor">Your favourite editor:</label></p>
            <p class="entries">
              <select id="registration.editor" name="registration.editor" onchange="toggle_select_hidden(this.id, 'editor_other')">
                <option value="">(please select)</option>
% for e in h.lca_rego['editors']:
                <option value="${ e }">${ e }</option>
% endfor
                <option value="other">other:</option>
              </select>
% if not registration or registration.editor in h.lca_rego['editors'] or registration.editor == '':
              <span id="editor_other" style="display: none">${ h.text('registration.editortext') }</span>
% else:
              <span id="editor_other" style="display: inline">${ h.text('registration.editortext') }</span>
% endif
            </p>
  </td>
  <td>

            <p class="label"><label for="registration.distro">Your favourite distro:</label></p>
            <p class="entries">
              <select id="registration.distro" name="registration.distro" onchange="toggle_select_hidden(this.id, 'distro_other')">
                <option value="">(please select)</option>
% for d in h.lca_rego['distros']:
                <option value="${ d }">${ d }</option>
% endfor
                <option value="other">other:</option>
              </select>
% if not registration or registration.distro in h.lca_rego['distros'] or registration.distro == '':
              <span id="distro_other" style="display: none">${ h.text('registration.distrotext') }</span>
% else:
              <span id="distro_other" style="display: inline">${ h.text('registration.distrotext') }</span>
% endif
            </p>
  </td>
</tr>
</table>

            <p class="label"><label for="registration.nick">Superhero name:</label></p>
            <p class="entries">${ h.text('registration.nick', size=30) }</p>
            <p class="note">Your IRC nick or other handle you go by.</p>

            <p class="label"><label for="registration.keyid">GnuPG/PGP Keyid:</label></p>
            <p class="entries">${ h.text('registration.keyid', size=10) }</p>
            <p class="note">If you have a GnuPG or PGP key that is stored on a public key server and would like to participate in the Conference Key Signing, please enter your keyid (e.g. A3D48B3C) here. More information about the key signing will be made available closer to the conference.</p>

            <p class="label"><label for="registration.planetfeed">Planet Feed:</label></p>
            <p class="entries">${ h.text('registration.planetfeed') }</p>
            <p class="note">If you have a Blog and would like it included in the conference planet, please specify an <em>LCA specific feed</em> to be included.</p>

            <p class="label"><label for="registration.silly_description">Description:</label>
            <blockquote>${ c.silly_description }</blockquote></p>
            ${ h.hidden('registration.silly_description') }
            ${ h.hidden('registration.silly_description_checksum') }
            <p class="note">This is a randomly chosen description for your name badge</p>

          </fieldset>
          <fieldset>
            <legend>&nbsp;</legend>
            <h2>Subscriptions</h2>

            <p class="entries">
              ${ h.checkbox('registration.signup.linuxaustralia') }
              <label for="registrationsignuplinuxaustralia">Sign up for membership with Linux Australia</label> <a href="http://www.linux.org.au/">(read more)</a>
            </p>

            <p class="entries">
              ${ h.checkbox('registration.signup.nzoss') }
              <label for="registrationsignupnzoss">Sign up for membership with the New Zealand Open Source Society</label> <a href="http://nzoss.org.nz/nzoss/about">(read more)</a>
            </p>

            <p class="entries">
              ${ h.checkbox('registration.signup.internetnz') }
              <label for="registrationsignupinternetnz">Sign up for membership with Internet NZ</label> <a href="http://www.internetnz.org.nz/membership">(read more)</a>
            </p>

            <p class="entries">
              ${ h.checkbox('registration.signup.announce') }
              <label for="registrationsignupannounce">Sign up to the low traffic <b>conference announcement list</b></label>
            </p>

            <p class="entries">
              ${ h.checkbox('registration.signup.chat') } 
              <label for="registrationsignupchat" >Sign up to the <b>conference attendees list</b></label>
            </p>
          </fieldset>

% if is_speaker:
          <fieldset>
            <legend>&nbsp;</legend>
            <h2>Speaker recording consent and release</h2>
            <p>As a service to Linux Australia members and to other interested Linux users,
            Linux Australia would like to make your presentation available to the public.
            This involves video­taping your talk, and offering the video/audio and slides
            (for download, or on CD­ROM).</p>

            <p>If you have allowed Linux Australia to publish your slides, there will
            be an upload mechanism closer to the conference. We will publish them under
            the Creative Commons Attribution License unless you have an equivalent
            preference that you let us know.</p>
          </fieldset>
% endif
