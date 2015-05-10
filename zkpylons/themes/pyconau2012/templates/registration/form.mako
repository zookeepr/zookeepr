<script type="text/javascript">
                   function ticketWarning(tickettype){
                   var str=/student/i;
                      if(tickettype.match(str)){
                         jQuery('#warningDiv').slideDown(1000);
                      }
                      else{
                         jQuery('#warningDiv').slideUp(1000);
                      }
                   }
                   function showRocketWarning(){
                     jQuery('#rocket_warning').slideDown(1000);
                     jQuery("#rocket_see_note").show();
                   }
</script>

<%
import datetime
import re
import array
%>

<p class="note">${ c.config.get('event_pricing_disclaimer') }</p>

        <fieldset id="personal">
          <legend>&nbsp;</legend>
          <h2>Personal Information</h2>

          <p class="note"><span class="mandatory">*</span> - Mandatory field</p>

          <p class="label">
            <b>Name:</b>
% if c.registration and c.registration.person:
          ${ c.registration.person.firstname }
% else:
          ${ c.signed_in_person.firstname }
% endif
% if c.registration and c.registration.person:
          ${ c.registration.person.lastname }
% else:
          ${ c.signed_in_person.lastname }
% endif
          </p>
          <p class="label">
            <b>Email address:</b>
% if c.registration and c.registration.person:
          ${ c.registration.person.email_address }
% else:
          ${ c.signed_in_person.email_address }
% endif
          </p>

%if c.config.get('personal_info', category='rego')['home_address'] == 'yes':
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

          <p class="label"><span class="mandatory">*</span><label for="person.postcode">Postcode/ZIP:</label></p>
          <p class="entries">${ h.text('person.postcode', size=40) }</p>
%else:
${ h.hidden('person.address1') }
${ h.hidden('person.address2') }
${ h.hidden('person.city') }
${ h.hidden('person.state') }
${ h.hidden('person.postcode') }
%endif

          <p class="label"><span class="mandatory">*</span><label for="person.country">Country:</label></p>
          <p class="entries">
            <select name="person.country">
% for country in h.countries():
              <option value="${country}">${ country }</option>
% endfor
            </select>
          </p>

<%
  is_speaker = c.signed_in_person.is_speaker()
%>

%if c.config.get('personal_info', category='rego')['phone'] == 'yes':
          <p class="label"><label for="person.mobile">Phone number (International Format):</label></p>
          <p class="entries">${ h.text('person.phone') }</p>

          <p class="label">
% if is_speaker:
            <span class="mandatory">*</span>
% endif
            <label for="person.mobile">Mobile/Cell number (International Format):</label>
          </p>
          <p class="entries">${ h.text('person.mobile') }</p>
%else:
${ h.hidden('person.phone') }
${ h.hidden('person.mobile') }
%endif

          <p class="label"><label for="person.company">Company:</label></p>
          <p class="entries">${ h.text('person.company', size=60) }</p>

        </fieldset>

        <fieldset id="voucher">
          <legend>&nbsp;</legend>
          <h2>Voucher</h2>

          <p class="label"><label for="registration.voucher_code">Voucher code:</label></p>
          <p class="entries">${ h.text('registration.voucher_code', size=15) }</p>
          <p class="note">If you have been provided with a voucher code, please enter it here.</p>

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
          <p class="description">${ category.description |n}</p>
          <input type="hidden" name="${'products.error.' + category.clean_name()}">
## Manual category display goes here:
%       if category.display_mode == 'shirt':
<%
           fields = dict()
           for product in products:
             results = re.match("^([a-zA-Z0-9']+)\s+(.*)$", product.description)
             gender = results.group(1)
             size = results.group(2)

             if gender not in fields:
               fields[gender] = []
             fields[gender].append((size, product))
           endfor
%>
          <table>
%           for gender in fields: 
            <tr>
              <th>&nbsp;</th>
%             for (size, product) in fields[gender]:
              <th>${ size }</th>
%             endfor
            </tr>
            <tr>
              <td>${ gender }</td>
%             for (size, product) in fields[gender]:

%               if not product.available():
              <td><span class="mandatory">SOLD&nbsp;OUT</span><br />${ h.hidden('products.product_' + product.clean_description(True) + '_qty', 0) }</td>
%               else:
%                 if category.display == 'qty':
              <td>${ h.text('products.product_' + product.clean_description(True) + '_qty', size=2) }</td>
%                 elif category.display == 'checkbox':
              <td>${ h.checkbox('products.product_' + product.clean_description(True) + '_checkbox') }</td>
%                 endif
%               endif
%             endfor
            </tr>
%           endfor
          </table>
%       elif category.display_mode == 'miniconf':
<%
          fields = {}
          for product in products:
            results = re.match("^([a-zA-Z0-9'_]+)\s+(.*)$", product.description)
            day = results.group(1).replace('_',' ')
            miniconf = results.group(2)

            if day not in fields:
              fields[day] = []
            fields[day].append((miniconf, product))
          endfor
%>
          <table>
            <tr>
%         for day in sorted(fields): 
              <th>${ day }</th>
%         endfor
            </tr>
            <tr>
%         for day in sorted(fields):
              <td>
%           for (miniconf, product) in sorted(fields[day]):
%             if category.display == 'qty':
                ${ h.text('products.product_' + product.clean_description(True) + '_qty', size=2, disabled=not product.available()) + ' ' + miniconf} 
%             elif category.display == 'checkbox':
                ${ h.checkbox('products.product_' + product.clean_description(True) + '_checkbox', label=miniconf, disabled=not product.available()) }
%             endif
%             if not product.available():
            <span class="mandatory">SOLD&nbsp;OUT</span>
%             elif product.cost != 0:
                - ${ h.integer_to_currency(product.cost) }
%             endif
            <br/>
%           endfor
              </td>
%         endfor
            </tr>
          </table>
%       elif category.display_mode == 'accommodation':
<%
          fields = {}
          for product in products:
            results = re.match("^([a-zA-Z0-9'_]+)\s+(.*)$", product.description)
            day = results.group(1).replace('_',' ')
            accom = results.group(2)

            if day not in fields:
              fields[day] = []
            fields[day].append((accom, product))
          endfor
%>
          <table>
            <tr>
%         for day in sorted(fields): 
              <th>${ day }</th>
%         endfor
            </tr>
            <tr>
%         for day in sorted(fields):
              <td>
%           for (accom, product) in sorted(fields[day]):
<div id="${ product.clean_description(True).replace(' ','_') + '_div'}">
%             if category.display == 'qty':
                ${ h.text('products.product_' + product.clean_description(True) + '_qty', size=2, disabled=not product.available()) + ' ' + accom} 
%             elif category.display == 'checkbox':
                ${ h.checkbox('products.product_' + product.clean_description(True) + '_checkbox', label=accom, disabled=not product.available()) }
%             endif
%             if not product.available():
            <span class="mandatory">SOLD&nbsp;OUT</span>
%             elif product.cost != 0:
                - ${ h.integer_to_currency(product.cost) }
%             endif
            <br /></div>
%           endfor
              </td>
%         endfor
            </tr>
          </table>
<script> 
$('div[id$="double_div"]').hide();
$('div[id$="double_breakfast_div"]').hide();
$('div[id$="single_breakfast_div"]').hide();
function accommdisplay() {
if (jQuery('input[id="breaky_accomm_option"]').attr('checked')) 
    {
    jQuery('div[id$="breakfast_div"]').show();
    jQuery('div[id$="double_div"]').hide();
    jQuery('div[id$="single_div"]').hide();
    }
else {
    jQuery('div[id$="breakfast_div"]').hide();
    jQuery('div[id$="double_div"]').show();
    jQuery('div[id$="single_div"]').show();
     }
if (jQuery('input[id="double_accomm_option"]').attr('checked'))
    {
    jQuery('div[id*="_single_"]').hide();
    }
  else
    {
    jQuery('div[id*="_double_"]').hide();
    }
 jQuery('input[id*="_accommodation_"]').attr('checked', false);
}
$('input[id$="accomm_option"]').change( function() {
accommdisplay();
});
</script>
%       elif category.display_mode == 'grid':
<table>
  <tr>
%           for product in products:
<%
               soldout = ''
               if not product.available():
                   soldout = '<span class="mandatory">SOLD&nbsp;OUT</span><br />'
%>
    <th>${ product.description }<br />${ soldout | n}(${ h.integer_to_currency(product.cost) })</th>
%           endfor
  </tr>
%           for product in products:
%             if category.display == 'qty':
    <td align="center">${ h.text('products.product_' + product.clean_description(True) + '_qty', size=2) }</td>
%             elif category.display == 'checkbox':
    <td align="center">${ h.checkbox('products.product_' + product.clean_description(True) + '_checkbox') }</td>
%             endif
%           endfor
</table>
%       elif category.display == 'radio':
         <p class="entries">
         <ul class="entries">
%         for product in products:
<%
               soldout = ''
               if not product.available():
                   soldout = ' <span class="mandatory">SOLD&nbsp;OUT</span> '
%> 

%              if category.name == "Ticket":
                <li> <label onclick="javascript: ticketWarning(' ${ product.description } ');"> ${ h.radio('products.category_' + category.clean_name(), str(product.id)) } ${ soldout |n}${ product.description } - ${ h.integer_to_currency(product.cost) }</label><br />
%                  if product.description.lower().find('student') > -1:

<div id="warningDiv">
         <div class="message message-information">
          <p>Your student Id will be validated at the registration desk. Your card must be current or at least expired at the end of the previous term/semester.</p>
         </div>
</div>
          <script type="text/javascript">
           jQuery("#warningDiv").hide();
          </script>
%                 endif
%              else:
          <li> <label> ${ h.radio('products.category_' + category.clean_name(), str(product.id)) } ${ soldout |n}${ product.description } - ${ h.integer_to_currency(product.cost) }</label><br />
%              endif
%         endfor
          </ul>
          </p>
%       elif category.display == 'select':
%         if category.name == 'Accommodation' and (len(category.products) == 0 or (len(category.products) == 1 and category.products[0].cost == 0)):
            <input type="hidden" name="products.category_${ category.clean_name() }">
%         else:
          <p class="entries">
            <select name="products.category_${ category.clean_name() }">
              <option value=""> - </option>
%           for product in products:
<%
               soldout = ''
               if not product.available():
                   soldout = ' SOLD&nbsp;OUT '
               endif
%>
              <option value="${ product.id }"> ${ soldout |n}${ product.description } - ${ h.integer_to_currency(product.cost) }</option>
%           endfor
            </select>
          </p>
%         endif
%       elif category.display == 'checkbox':
%           for product in products:
<%
               soldout = ''
               if not product.available():
                   soldout = ' <span class="mandatory">SOLD&nbsp;OUT</span> '
%>
         <p class="entries">${ h.checkbox('products.product_' + product.clean_description(True) + '_checkbox', label=soldout + ' ' + product.description + ' - ' + h.integer_to_currency(product.cost)) }</p>
%           endfor
%       elif category.display == 'qty':
%           for product in products:
<%
               soldout = ''
               if not product.available():
                   soldout = ' <span class="mandatory">SOLD&nbsp;OUT</span> '
%>
          <p>${ soldout |n}${ product.description } ${ h.text('products.product_' + product.clean_description(True) + '_qty', size=2) } x ${ h.integer_to_currency(product.cost) }</p>
%           endfor
%       endif
%       if category.name == 'Accommodation':
%         if len(category.products) == 0 or (len(category.products) == 1 and category.products[0].cost == 0):
          <p class="note">Please see the
          <a href="/register/accommodation" target="_blank">accommodation page</a>
          for discounted rates for delegates. You <strong>must</strong> book
          your accommodation directly through the accommodation providers
          yourself. Registering for the conference <strong>does not</strong>
          book your accommodation.</p>
%         else:
          <p>Please see the <a href="/register/accommodation" target="_blank">accommodation page</a> for prices and details.</p>

%         endif
%       elif category.name == "Partners Programme":
          <p class="label"><span class="mandatory">#</span><label for="registration.partner_name">Your partner's name:</label></p>
          <p class="entries">${ h.text('products.partner_name', size=50) }</p>
          <p class="note">#If your partner will be participating in the programme, then this field is required so that our Partners Programme manager can contact them.</p>
          <p class="label"><span class="mandatory">#</span><label for="registration.partner_email">Your partner's email address:</label></p>
          <p class="entries">${ h.text('products.partner_email', size=50) }</p>
          <p class="note">#If your partner will be participating in the programme, then this field is required so that our Partners Programme manager can contact them.</p>
          <p class="label"><span class="mandatory">#</span><label for="registration.partner_mobile">Your partner's mobile (if known, in international format, otherwise enter "<b>unknown</b>"):</label></p>
          <p class="entries">${ h.text('products.partner_mobile', size=50) }</p>
          <p class="note">A Partners Programme shirt is included with every adult partner ticket. Please indicate the appropriate number and sizes in the T-Shirt Section (above).</p>
%       endif
%     if category.note:
        <p class="note">${ category.note | n }</p>
%     endif
        </fieldset>
%   endif
% endfor

        <fieldset>
          <legend>&nbsp;</legend>
          <h2>Further Information</h2>

          <p class="label"><span class="mandatory">*</span> <label for="registration.over18">Are you over 18?</label></p>
          <p class="entries">
            ${ h.radio('registration.over18', 1, label='Yes') }<br />
            ${ h.radio('registration.over18', 0, label='No') } <br />
           </p>
          <p class="note">Being under 18 will not stop you from registering. We need to know whether you are over 18 to allow us to cater for you at venues that serve alcohol.</p>

          <p class="label"><label for="registration.diet">Dietary requirements:</label></p>
          <p class="entries">${ h.text('registration.diet', size=60) }</p>

          <p class="label"><label for="registration.special">Other special requirements:</label></p>
          <p class="entries">${ h.text('registration.special', size=60) }</p>
          <p class="note">Please enter any requirements if necessary; access requirements, etc.</p>
% if c.config.get('ask_past_confs', category='rego'):
             <p class="label"><label for="registration.prevlca">Have you attended any Python conferences before?</label></p>
            <p class="entries">
            <table>
              <tr>
                <td>
%     for (year, desc) in c.config.get('past_confs', category='rego'):
       <% label = 'registration.prevlca.%s' % year %>
                <label>${ h.checkbox(label) } ${ desc }</label><br />
%     endfor
                </td>
              </tr>
            </table>
            </p>
% endif
          </fieldset>
% if c.config.get('lca_optional_stuff', category='rego'):
          <fieldset>
            <legend>&nbsp;</legend>
            <h2>Optional</h2>
<script src="/silly.js"></script>
<table>
<tr>
  <th>Your favourite shell</th>
  <th>Your favourite editor</th>
  <th>Your favourite distro</th>
  <th>Your favourite vcs</th>
</tr>
<tr>
  <td>
            <p class="entries">
              <select id="registration.shell" name="registration.shell" onchange="toggle_select_hidden(this.id, 'shell_other')">
                <option value="">(please select)</option>
% for s in c.config.get('shells', category='rego'):
                <option value="${s}">${ s }</option>
% endfor
                <option value="other">other</option>
              </select>
            </p>

% if not c.registration or c.registration.shell in c.config.get('shells', category='rego') or c.registration.shell == '':
<span id="shell_other" style="display: none">
% else:
<span id="shell_other" style="display: inline">
% endif
  <p class="entries">${ h.text('registration.shelltext', size=12) }</entries></p>
</span>
  </td>

  <td>
            <p class="entries">
              <select id="registration.editor" name="registration.editor" onchange="toggle_select_hidden(this.id, 'editor_other')">
                <option value="">(please select)</option>
% for e in c.config.get('editors', category='rego'):
                <option value="${ e }">${ e }</option>
% endfor
                <option value="other">other</option>
              </select>
            </p>

% if not c.registration or c.registration.editor in c.config.get('editors', category='rego') or c.registration.editor == '':
<span id="editor_other" style="display: none">
% else:
<span id="editor_other" style="display: inline">
% endif
  <p class="entries">${ h.text('registration.editortext', size=12) }</entries></p>
</span>
  </td>

  <td>
            <p class="entries">
              <select id="registration.distro" name="registration.distro" onchange="toggle_select_hidden(this.id, 'distro_other')">
                <option value="">(please select)</option>
% for d in c.config.get('distros', category='rego'):
                <option value="${ d }">${ d }</option>
% endfor
                <option value="other">other</option>
              </select>
            </p>

% if not c.registration or c.registration.distro in c.config.get('distros', category='rego') or c.registration.distro == '':
<span id="distro_other" style="display: none">
% else:
<span id="distro_other" style="display: inline">
% endif
  <p class="entries">${ h.text('registration.distrotext', size=12) }</entries></p>
</span>
  </td>
  <td>
            <p class="entries">
              <select id="registration.vcs" name="registration.vcs" onchange="toggle_select_hidden(this.id, 'vcs_other')">
                <option value="">(please select)</option>
% for s in c.config.get('vcses', category='rego'):
                <option value="${s}">${ s }</option>
% endfor
                <option value="other">other</option>
              </select>
            </p>

% if not c.registration or c.registration.vcs in c.config.get('vcses', category='rego') or c.registration.vcs == '':
<span id="vcs_other" style="display: none">
% else:
<span id="vcs_other" style="display: inline">
% endif
  <p class="entries">${ h.text('registration.vcstext', size=12) }</entries></p>
</span>
  </td>
</tr>
</table>

            <p class="label"><label for="registration.nick">Superhero name:</label></p>
            <p class="entries">${ h.text('registration.nick', size=30) }</p>
            <p class="note">Your IRC nick or other handle you go by.</p>

% if c.config.get('pgp_collection', category='rego') != 'no':
            <p class="label"><label for="registration.keyid">GnuPG/PGP Keyid:</label></p>
            <p class="entries">${ h.text('registration.keyid', size=10) }</p>
            <p class="note">If you have a GnuPG or PGP key then please enter its short key id here and we will print it on your badge.</p>
% endif

            <p class="label"><label for="registration.planetfeed">Planet Feed:</label></p>
            <p class="entries">${ h.text('registration.planetfeed', size=50) }</p>
            <p class="note">If you have a blog and would like it included in the ${ c.config.get('event_name') } planet, please specify an <b>${ c.config.get('event_name') } specific feed</b> to be included. (This is the URL of the RSS feed.)</p>

            <p class="label"><label for="registration.silly_description">Description:</label>
            <blockquote class="entries">${ c.silly_description }</blockquote></p>
            ${ h.hidden('registration.silly_description') }
            ${ h.hidden('registration.silly_description_checksum') }
            <p class="note">This is a randomly chosen description for your name badge</p>

          </fieldset>
% endif
          <fieldset>
            <legend>&nbsp;</legend>
            <h2>Subscriptions</h2>
             <p class="note">Tick below to sign up for any of the following:</p>

            <p class="entries">
            <ul class="entries">
              <li> <label>${ h.checkbox('registration.signup.announce') } the low traffic <b>${ c.config.get('event_name') }  announcement list</b></label>

              <li> <label>${ h.checkbox('registration.signup.chat') } the <b>${ c.config.get('event_name') } attendees list</b></label>
            </ul>
            </p>
          </fieldset>


