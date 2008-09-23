        <fieldset id="person">
          <h2>About yourself</h2>

% if not c.signed_in_person:
          <p class="note"><span class="mandatory">*</span> - Mandatory field</p>
% #endif
          <p class="label">
% if not c.signed_in_person:
            <span class="mandatory">*</span>
% #endif
            <label for="person.firstname">Your first name:</label>
          </p>
% if c.registration and c.registration.person:
          <p><% c.registration.person.firstname | h %></p>
% elif c.signed_in_person:
          <p><% c.signed_in_person.firstname | h %></p>
% else:
          <p class="entries"><% h.textfield('person.firstname', size=40) %></p>
% #endif

          <p class="label">
% if not c.signed_in_person:
            <span class="mandatory">*</span>
% #endif
            <label for="person.lastname">Your last name:</label>
          </p>
% if c.registration and c.registration.person:
          <p><% c.registration.person.lastname | h %></p>
% elif c.signed_in_person:
          <p><% c.signed_in_person.lastname | h %></p>
% else:
          <p class="entries"><% h.textfield('person.lastname', size=40) %></p>
% #endif

          <p class="label">
% if not c.signed_in_person:
            <span class="mandatory">*</span>
% #endif
            <label for="person.email_address">Email address:</label>
          </p>
% if c.registration and c.registration.person:
          <p><% c.registration.person.email_address | h %></p>
% elif c.signed_in_person:
          <p><% c.signed_in_person.email_address | h %></p>
% else:
          <p class="entries"><% h.textfield('person.email_address', size=40) %></p>
% #endif
          <p class="note">Your email address will only be used to correspond with you, and is your login name for the website.  It will not be shown or used otherwise.</p>
% if not c.signed_in_person:

          <p class="label"><span class="mandatory">*</span><label for="person.password">Choose a password:</label></p>
          <p class="entries"><% h.password_field("person.password", size=40) %></p>

          <p class="label"><span class="mandatory">*</span><label for="person.password_confirm">Confirm your password:</label></p>
          <p class="entries"><% h.password_field("person.password_confirm", size=40) %></p>
% #endif
        </fieldset>

        <fieldset id="personal">
          <h2>Personal Information</h2>

          <p class="note"><span class="mandatory">*</span> - Mandatory field</p>

          <p class="label"><span class="mandatory">*</span><label for="person.address">Address:</label></p>
          <p class="entries">
            <% h.textfield('person.address1', size=40) %>
            <br>
            <% h.textfield('person.address2', size=40) %>
          </p>

          <p class="label"><span class="mandatory">*</span><label for="person.city">City/Suburb:</label></p>
          <p class="entries"><% h.textfield('person.city', size=40) %></p>

          <p class="label"><label for="person.state">State/Province:</label></p>
          <p class="entries"><% h.textfield('person.state', size=40) %></p>

          <p class="label"><span class="mandatory">*</span><label for="person.country">Country:</label></p>
          <p class="entries">
            <select name="person.country">
% for country in h.countries():
              <option value="<%country%>"><% country %></option>
% #endfor
            </select>
          </p>

          <p class="label"><span class="mandatory">*</span><label for="person.postcode">Postcode/ZIP:</label></p>
          <p class="entries"><% h.textfield('person.postcode', size=40) %></p>

% if 'signed_in_person_id' in session:
%   is_speaker = c.signed_in_person.is_speaker()
% else:
%   is_speaker = False
% #endif

          <p class="label"><label for="person.mobile">Phone number:</label></p>
          <p class="entries"><% h.textfield('person.phone') %></p>

          <p class="label">
% if is_speaker:
            <span class="mandatory">*</span>
% #endif
            <label for="person.mobile">Mobile/Cell number:</label>
          </p>
          <p class="entries"><% h.textfield('person.mobile') %></p>

          <p class="label"><label for="person.company">Company:</label></p>
          <p class="entries"><% h.textfield('person.company', size=60) %></p>

        </fieldset>
% for category in c.product_categories:
%   all_products = category.available_products(c.signed_in_person)
%   products = []
%   for product in all_products:
%       if c.product_available(product):
%           products.append(product)
%       #endif
%   #endfor
%   if len(products) > 0:

        <fieldset id="<% h.computer_title(category.name) %>">
          <h2><% category.name.title() %></h2>
          <p class="note"><% category.description %></p>
# Manual category display goes here:
%       if category.name == 'Shirt':
#%           # fields need to be exactly the same order as the shirts in the DB, this just replaces their name.
#%           # Number of items in the row must be the same for each row
%           fields = [("Men's Short Sleeved Shirt", ['S', 'M', 'L', 'XL', 'XXL', 'XXXL', 'XXXXL', 'XXXXXL']),("Women's Short Sleeved Shirt", ['S', 'M', 'L', 'XL', 'XXL', 'XXXL', 'XXXXL', 'XXXXXL'])]
%           i = j = 0
          <p>All shirts are $20 each and made in Tasmania. More details on shirt sizes can be found on the information page.</p>
          <table>
            <tr><th>&nbsp;</th><th>S</th><th>M</th><th>L</th><th>XL</th><th>XXL</th><th>XXXL</th><th>XXXXL</th><th>XXXXXL</th></tr>
            <tr><td><% fields[0][0] %></td>
%           for product in products:
%               if j == len(fields[i][1]):
%                   i += 1
%                   j = 0
            </tr><tr><td><% fields[i][0] %></td>
%               #endif
            <td><% h.text_field('products.product_' + str(product.id) + '_qty', size=2) %></td>
%               j += 1
%           #endfor
          </tr></table>
%       elif category.display == 'radio':
%           for product in products:
          <p><label><% h.radio_button('products.category_' + str(category.id), product.id) %><% product.description %> - <% h.number_to_currency(product.cost/100.0) %></label></p>
%           #endfor
%       elif category.display == 'select':
          <p class="entries">
            <select name="products.category_<% category.id %>">
              <option value=""> - </option>
%           for product in products:
              <option value="<% product.id %>"> <% product.description %> - <% h.number_to_currency(product.cost/100.0) %></option>
%           #endfor
            </select>
          </p>
%       elif category.display == 'checkbox':
%           for product in products:
          <p><label><% h.check_box('products.product_' + str(product.id)) %><% product.description %> - <% h.number_to_currency(product.cost/100.0) %></label></p>
%           #endfor
%       elif category.display == 'qty':
%           for product in products:
          <p><% product.description %> <% h.text_field('products.product_' + str(product.id) + '_qty', size=2) %> x <% h.number_to_currency(product.cost/100.0) %></p>
%           #endfor
%       #endif
%       if category.name == 'Accomodation':
          <p>Please see <a href="/register/accommodation">the accomodation page</a> for prices and details, including how to book your Wrest Point room at LCA09 rates.</p>
          <p class="label"><span class="mandatory">*</span><label for="registration.checkin">Check in on:</label></p>
          <p class="entries">
            <select name="registration.checkin">
%           dates = [(d, 1) for d in range(18,26)]
%           for (day, month) in dates:
              <option value="<% day %>"><% datetime.datetime(2009, month, day).strftime('%A, %e %b') %></option>
%           #endfor
            </select>
          </p>

          <p class="label"><span class="mandatory">*</span><label for="registation.checkout">Check out on:</label></p>
          <p class="entries">
            <select name="registration.checkout">
%           for day, month in dates[1:]:
              <option value="<% day %>" ><% datetime.datetime(2009, month, day).strftime('%A, %e %b') %></option>
%           #endfor
            </select>
          </p>
%       elif category.name == 'Partners Programme':
          <p class="label"><label for="registration.partner_email">Your partner's email address:</label></p>
          <p class="entries"><% h.textfield('products.partner_email', size=50) %></p>
          <p class="note">If your partner will be participating in the programme, please enter their email address here so that our Partners Programme manager can contact them.</p>
%       #endif
        </fieldset>
%   #endif
% #endfor

        <fieldset>
          <h2>Further Information</h2>

          <p class="label"><label for="registration.voucher_code">Voucher Code</label></p>
          <p class="entries"><% h.textfield('registration.voucher_code', size=15) %></p>
          <p class="note">If you have been provided with a voucher code enter it here.</p>

          <p class="label"><label for="registration.diet">Dietary requirements:</label></p>
          <p class="entries"><% h.textfield('registration.diet', size=100) %></p>

          <p class="label"><label for="registration.special">Other special requirements</label></p>
          <p class="entries"><% h.textfield('registration.special', size=100) %></p>
          <p class="note">Please enter any requirements if necessary; access requirements, etc.</p>

          <p class="label"><label for="registration.miniconfs">Preferred mini-confs:</label></p>
          <p class="entries">
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
%       label = 'registration.miniconf.%s' % miniconf.replace(' ', '_').replace('.', '_')
                  <% h.check_box(label) %>
                  <label for="<% label %>"><% miniconf %></label>
                  <br>
%   #endfor
                </td>
% #endfor
              </tr>
            </table>

            <p class="note">Please check the <% h.link_to('mini-confs', url="/programme/mini-confs") %> page for details on each event. You can choose to attend multiple mini-confs in the one day, as the schedules will be published ahead of the conference for you to swap sessions.</p>

            <p class="label"><label for="registration.opendaydrag">How many people are you bringing to Open Day?</label></p>
            <p class="entries"><% h.textfield('registration.opendaydrag', size=10) %></p>
            <p class="note">
              <!-- <% h.link_to("Open Day", url="/programme/open-day", popup=True) %> -->
              Open Day
              is open to friends and family, and is targeted to a non-technical
              audience.  If you want to show off FOSS culture to some people, you can
              give us an idea of how many people to expect.
            </p>

            <p class="label"><label for="registration.shell">Your favourite shell:</label></p>
            <p class="entries">
              <select id="registration.shell" name="registration.shell" onchange="toggle_select_hidden(this.id, 'shell_other')">
                <option value="">(please select)</option>
% for s in h.lca_rego['shells']:
                <option value="<%s%>"><% s %></option>
% #endfor
                <option value="other">other:</option>
              </select>
% if defaults['registration.shell'] in h.lca_rego['shells'] or defaults['registration.shell'] == '':
              <span id="shell_other" style="display: none"><% h.textfield('registration.shelltext') %></span>
% else:
              <span id="shell_other" style="display: inline"><% h.textfield('registration.shelltext') %></span>
% #endif
            </p>

            <p class="label"><label for="registration.editor">Your favourite editor:</label></p>
            <p class="entries">
              <select id="registration.editor" name="registration.editor" onchange="toggle_select_hidden(this.id, 'editor_other')">
                <option value="">(please select)</option>
% for e in h.lca_rego['editors']:
                <option value="<% e %>"><% e %></option>
% #endfor
                <option value="other">other:</option>
              </select>
% if defaults['registration.editor'] in h.lca_rego['editors'] or defaults['registration.editor'] == '':
              <span id="editor_other" style="display: none"><% h.textfield('registration.editortext') %></span>
% else:
              <span id="editor_other" style="display: inline"><% h.textfield('registration.editortext') %></span>
% #endif
            </p>

            <p class="label"><label for="registration.distro">Your favourite distro:</label></p>
            <p class="entries">
              <select id="registration.distro" name="registration.distro" onchange="toggle_select_hidden(this.id, 'distro_other')">
                <option value="">(please select)</option>
% for d in h.lca_rego['distros']:
                <option value="<% d %>"><% d %></option>
% #endfor
                <option value="other">other:</option>
              </select>
% if defaults['registration.distro'] in h.lca_rego['distros'] or defaults['registration.distro'] == '':
              <span id="distro_other" style="display: none"><% h.textfield('registration.distrotext') %></span>
% else:
              <span id="distro_other" style="display: inline"><% h.textfield('registration.distrotext') %></span>
% #endif
            </p>

            <p class="label"><label for="registration.nick">Superhero name:</label></p>
            <p class="entries"><% h.textfield('registration.nick', size=30) %></p>
            <p class="note">Your IRC nick or other handle you go by.</p>

            <p class="label"><label for="registration.prevlca">Have you attended linux.conf.au before?</label></p>
            <p class="entries">
% for (year, desc) in h.lca_rego['past_confs']:
%   label = 'registration.prevlca.%s' % year
                <br>
                <% h.check_box(label) %>
                <label for="<% label %>"><% desc %></label>
% #endfor
            </p>

            <p class="label"><label for="registration.silly_description">Description:</label></p>
            <script src="/silly.js"></script>
            <blockquote><p id='silly_description'><% defaults['registration.silly_description'] %></p></blockquote>
#            <p><% h.button_to_function('New Description', function='silly_description()') %></p>
            <% h.hidden_field('registration.silly_description') %>
            <% h.hidden_field('registration.silly_description_checksum') %>
            <p class="note">This is a randomly chosen description for your name badge</p>
          </fieldset>

          <fieldset>
            <h2>Subscriptions</h2>

            <p class="entries">
              <% h.check_box('registration.lasignup') %>
              <label for="registration.lasignup">I want to sign up for (free) Linux Australia membership!</label>
            </p>

            <p class="entries">
              <% h.check_box('registration.announcesignup') %>
              <label for="registration.announcesignup">I want to sign up to the low traffic conference announcement mailing list!</label>
            </p>

            <p class="entries">
              <% h.check_box('registration.delegatesignup') %>
              <label for="registration.delegatesignup">I want to sign up to the conference attendees mailing list!</label>
            </p>
          </fieldset>

% if is_speaker:
          <fieldset>
            <h2>Speaker recording consent and release</h2>
            <p>As a service to Linux Australia members and to other interested Linux users,
            Linux Australia would like to make your presentation available to the public.
            This involves video­taping your talk, and offering the video/audio and slides
            (for download, or on CD­ROM).</p>

            <p class="entries">
              <% h.check_box('registration.speaker_record') %>
              <label for="registration.speaker_record">I allow Linux Australia to record my presentation</label>
            </p>

            <p class="entries">
              <% h.check_box('registration.speaker_video_release') %>
              <label for="registration.speaker_video_release">I allow Linux Australia to
              release my video under the Creative Commons ShareAlike License</label>
            </p>

            <p class="entries">
              <% h.check_box('registration.speaker_slides_release') %>
              <label for="registration.speaker_slides_release">I allow Linux Australia to share my slides</label>
            </p>

            <p>If you have allowed Linux Australia to publish your slides, there will
            be an upload mechanism closer to the conference. We will publish them under
            the Creative Commons Attribution License unless you have an equivalent
            preference that you let us know.</p>
          </fieldset>
% #endif
<%args>
defaults
errors
</%args>
<%init>
import datetime
</%init>
