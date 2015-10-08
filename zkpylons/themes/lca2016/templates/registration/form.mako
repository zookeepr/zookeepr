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

<p class="note">${ h.lca_info['event_pricing_disclaimer'] }</p>

        <fieldset id="personal">
          <h2>Personal Information</h2>

            <div class="row form-group"> 
                <label for="name" class="col-sm-2 control-label">Name</label>
                <div class="input-group col-sm-10">
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
                </div>
            </div>
            
            <div class="row form-group"> 
                <label for="email" class="col-sm-2 control-label">Email</label>
                <div class="input-group col-sm-10">
% if c.registration and c.registration.person:
          ${ c.registration.person.email_address }
% else:
          ${ c.signed_in_person.email_address }
% endif
                </div>
            </div>

%if h.lca_rego['personal_info']['home_address'] == 'yes':
    <div class="row form-group">
        <label for="personaddress1" class="col-sm-2 control-label">Address 1</label>
        <div class="input-group col-sm-10">
            <input type="text" id="personaddress1" class="form-control" placeholder="Address" name="person.address1" required />
            <span class="input-group-addon" id="basic-addon2">required</span>
        </div>
        <div class="help-block with-errors"></div>
    </div>
    <div class="row form-group">
        <label for="personaddress1" class="col-sm-2 control-label">Address 2</label>
        <div class="input-group col-sm-10">
            <input type="text" id="personaddress2" class="form-control" placeholder="Additional Address" name="person.address2" />
        </div>
    </div>

    <div class="row form-group">
        <label for="personcity" class="col-sm-2 control-label">City / Suburb</label>
        <div class="input-group col-sm-10">
            <input type="text" id="personcity" class="form-control" placeholder="City/Suburb" name="person.city" required />
            <span class="input-group-addon" id="basic-addon2">required</span>
        </div>
        <div class="help-block with-errors"></div>
    </div>

    <div class="row form-group">
        <label for="personstate" class="col-sm-2 control-label">State</label>
        <div class="input-group col-sm-10">
            <input type="text" id="personstate" class="form-control" placeholder="State" name="person.state" />
            <span class="input-group-addon" id="basic-addon2">required</span>
        </div>
        <div class="help-block with-errors"></div>
    </div>
    
    <div class="row form-group">
        <label for="personpostcode" class="col-sm-2 control-label">Postcode/ZIP</label>
        <div class="input-group col-sm-10">
            <input type="text" id="personpostcode" class="form-control" placeholder="Postcode/ZIP" name="person.postcode" required />
            <span class="input-group-addon" id="basic-addon2">required</span>
        </div>
        <div class="help-block with-errors"></div>
    </div>

%else:
${ h.hidden('person.address1') }
${ h.hidden('person.address2') }
${ h.hidden('person.city') }
${ h.hidden('person.state') }
${ h.hidden('person.postcode') }
%endif

    <div class="row form-group">
        <label for="personcountry" class="col-sm-2 control-label">Country</label>
        <div class="input-group col-sm-10">
            <select id="personcountry" class="form-control" placeholder="Country" name="person.country">
%for country in h.countries():
% if country == 'australia':
            <option selected="selected" value="${ country }">${ country }</option>
% else:
            <option value="${ country }">${ country }</option>
% endif
%endfor
            </select>
        </div>
    </div>

<%
  is_speaker = c.signed_in_person.is_speaker()
%>

%if h.lca_rego['personal_info']['phone'] == 'yes':

    <div class="row form-group">
        <label for="person.phone" class="col-sm-2 control-label">Phone number:</label>
        <div class="input-group col-sm-10">
%if is_speaker:
            <input type="text" id="personphone" class="form-control" placeholder="Please use international Format" name="person.phone" required/>
            <span class="input-group-addon" id="basic-addon2">required</span>
%else:
            <input type="text" id="personphone" class="form-control" placeholder="Please use international Format" name="person.phone" />
%endif
        </div>
    </div>
    
    <div class="row form-group">
        <label for="person.mobile" class="col-sm-2 control-label">Mobile/Cell number</label>
        <div class="input-group col-sm-10">
            <input type="text" id="personmobile" class="form-control" placeholder="Please use international Format" name="person.mobile" />
        </div>
    </div>
    
%else:
${ h.hidden('person.phone') }
${ h.hidden('person.mobile') }
%endif

    <div class="row form-group">
        <label for="personcompany" class="col-sm-2 control-label">Company</label>
        <div class="input-group col-sm-10">
            <input type="text" id="personcompany" class="form-control" placeholder="Company" name="person.company" />
        </div>
    </div>

        </fieldset>

        <fieldset id="voucher">
          <h2>Voucher</h2>
            <div class="row form-group">
                <label for="proposaltype" class="col-sm-2 control-label">Voucher code:</label>
                <div class="col-sm-10">
                    <input type="text" id="registrationvoucher_code" class="form-control" placeholder="If you have been provided with a voucher code, please enter it here." name="registration.voucher_code" />
                </div>
            </div>
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
          <table class="table">
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
          <table class="table">
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
				<div class="checkbox">
      				<label>
        			<input type="checkbox" name="${ 'products.product_' + product.clean_description(True) + '_checkbox'}" id="${ 'productsproduct_' + product.clean_description(True).replace(" ", "_").lower() + '_checkbox' }">
        			${ miniconf }
%				if not product.available():
            <span class="mandatory">SOLD&nbsp;OUT</span>
%   	        elif product.cost != 0:
                - ${ h.integer_to_currency(product.cost) }
%       	    endif
      				</label>
    			</div>
                <!--${ h.checkbox('products.product_' + product.clean_description(True) + '_checkbox', label=miniconf, disabled=not product.available()) }-->
%             endif
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
          <table class="table">
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
<table class="table">
  <tr>
%           for product in products:
<%
               soldout = ''
               if not product.available():
                   soldout = '<span class="mandatory">SOLD&nbsp;OUT</span><br />'
%>
    <th><center>${ product.description }<br />${ soldout | n}(${ h.integer_to_currency(product.cost) })</center></th>
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
    <div class="row form-group">
      <label for="proposaltype" class="col-sm-2 control-label"></label>
      <div class="col-sm-10">
%         for product in products:
<%
               soldout = ''
               if not product.available():
                   soldout = ' <span class="mandatory">SOLD&nbsp;OUT</span> '
%>

%              if category.name == "Ticket":
    			<div class="radio">
      				<label onclick="javascript: ticketWarning(' ${ product.description } ');">
        			<input type="radio" name="${ 'products.category_' + category.clean_name()}" id="products.category_${ category.clean_name() + "_" + str(product.id) }" onclick = "">
        			${ h.radio('products.category_' + category.clean_name(), str(product.id)) } ${ soldout |n}${ product.description } - ${ h.integer_to_currency(product.cost) }
%                  if product.description.lower().find('student') > -1:
<div id="warningDiv">
         <div class="message message-information">
          <p>Your student Id will be validated at the registration desk. Your card must be current or at least expired at the end of the previous term/semester.</p>
         </div>
</div>
          <script type="text/javascript">
           jQuery("#warningDiv").hide();
          </script>
%                  endif
      				</label>
    			</div>
                
%              else:
    			<div class="radio">
      				<label>
        			<input type="radio" name="${ 'products.category_' + category.clean_name()}" id="products.category_${ category.clean_name() + "_" + str(product.id) }" onclick = "">
        			${ h.radio('products.category_' + category.clean_name(), str(product.id)) } ${ soldout |n}${ product.description } - ${ h.integer_to_currency(product.cost) }
      				</label>
    			</div>
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
				<div class="checkbox">
      				<label>
        			<input type="checkbox" name="${ 'products.product_' + product.clean_description(True) + '_checkbox'}" id="products.category_${ category.clean_name() + "_" + str(product.id) }" onclick = "">
        			${ soldout |n}${ product.description } - ${ h.integer_to_currency(product.cost) }
      				</label>
    			</div>
        <!-- <p class="entries">${ h.checkbox('products.product_' + product.clean_description(True) + '_checkbox', label=soldout + ' ' + product.description + ' - ' + h.integer_to_currency(product.cost)) }</p>-->
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
%       elif category.name == "Partners' Programme":

    <div class="row form-group">
        <label for="products.partner_name" class="col-sm-2 control-label">Your partner's name</label>
        <div class="input-group col-sm-10">
            <input type="text" id="productspartner_name" class="form-control" placeholder="" name="products.partner_name" />
        </div>
    </div>
    <div class="row form-group">
        <label for="products.partner_email" class="col-sm-2 control-label">Your partner's email</label>
        <div class="input-group col-sm-10">
            <input type="text" id="productspartner_email" class="form-control" placeholder="If your partner will be participating in the programme, then this field is required so that our Partners Programme manager can contact them." name="products.partner_email" />
        </div>
    </div>
    <div class="row form-group">
        <label for="products.partner_mobile" class="col-sm-2 control-label">Your partner's mobile number</label>
        <div class="input-group col-sm-10">
            <input type="text" id="productspartner_mobile" class="form-control" placeholder="Enter number in international format. If you don't know the number, type "unknown"." name="products.partner_mobile" />
        </div>
    </div>

%       endif
%     if category.note:
        <p class="note">${ category.note | n }</p>
%     endif
        </fieldset>
%   endif
% endfor

        <fieldset>
          <h2>Further Information</h2>

		<div class="row form-group">
      		<label for="proposaltype" class="col-sm-2 control-label">Are you over 18?</label>
      		<div class="col-sm-10">
    			<div class="radio">
      				<label>
        				<input type="radio" name="registration.over18" id="registration.over18_1" value="1">
        				Yes
      				</label>
    			</div>
    			<div class="radio">
      				<label>
        				<input type="radio" name="registration.over18" id="registration.over18_0" value="0">
        				No
      				</label>
    			</div>
    		</div>
<p class="note">Being under 18 will not stop you from registering. We need to know whether you are over 18 to allow us to cater for you at venues that serve alcohol.</p>
    	</div>


    <div class="row form-group">
        <label for="registration.diet" class="col-sm-2 control-label">Dietary requirements</label>
        <div class="input-group col-sm-10">
            <input type="text" id="registrationdiet" class="form-control" placeholder="" name="registration.diet" />
        </div>
    </div>
    
    <div class="row form-group">
        <label for="registration.special" class="col-sm-2 control-label">Other Special requirements</label>
        <div class="input-group col-sm-10">
            <input type="text" id="registrationspecial" class="form-control" placeholder="Please enter any requirements if necessary; access requirements, etc." name="registration.special" />
        </div>
    </div>
          
% if h.lca_rego['ask_past_confs']:
            <h3>Have you attended ${ h.lca_info['event_generic_name'] } before?</h3>
            <p class="entries">
            <table class="table">
              <tr>
                <td>
%     for (year, desc) in h.lca_rego['past_confs']:
<div class="checkbox">
      				<label>
      				<% label1 = 'registration.prevlca.%s' % year %>
      				<% label2 = 'registrationprevlca%s' % year %>
        			<input type="checkbox" name="${ label1 }" id="${ label2 }" value="1">
        			${ desc }
      				</label>
    			</div>

%     endfor
                </td>
              </tr>
            </table>
            </p>
% endif
          </fieldset>
% if h.lca_rego['lca_optional_stuff'] == 'yes':
          <fieldset>
              <h2>Optional</h2>
<script src="/silly.js"></script>


    <div class="row form-group">
        <label for="registration.shell" class="col-sm-4 control-label">Your favourite shell</label>
        <div class="input-group col-sm-6">
            <select id="registration.shell" class="form-control" placeholder="" name="registration.shell">
% for s in h.lca_rego['shells']:
                <option value="${s}">${ s }</option>
% endfor
            </select>
        </div>
    </div>
    
    <div class="row form-group">
        <label for="registration.editor" class="col-sm-4 control-label">Your favourite editor</label>
        <div class="input-group col-sm-6">
            <select id="registration.editor" class="form-control" placeholder="" name="registration.editor">
% for s in h.lca_rego['editors']:
                <option value="${s}">${ s }</option>
% endfor
            </select>
        </div>
    </div>
    
    <div class="row form-group">
        <label for="registration.distro" class="col-sm-4 control-label">Your favourite distro</label>
        <div class="input-group col-sm-6">
            <select id="registration.distro" class="form-control" placeholder="" name="registration.distro">
% for s in h.lca_rego['distros']:
                <option value="${s}">${ s }</option>
% endfor
            </select>
        </div>
    </div>

    <div class="row form-group">
        <label for="registration.vcs" class="col-sm-4 control-label">Your favourite VCS</label>
        <div class="input-group col-sm-6">
            <select id="registration.vcs" class="form-control" placeholder="" name="registration.vcs">
% for s in h.lca_rego['vcses']:
                <option value="${s}">${ s }</option>
% endfor
            </select>
        </div>
    </div>

    <div class="row form-group">
        <label for="registration.nick" class="col-sm-4 control-label">Superhero name</label>
        <div class="input-group col-sm-6">
            <input type="text" id="registrationnick" class="form-control" placeholder="Your IRC nick or other handle you go by" name="registration.nick" />
        </div>
    </div>

% if h.lca_rego['pgp_collection'] != 'no':
    <div class="row form-group">
        <label for="registration.keyid" class="col-sm-4 control-label">GnuPG/PGP Keyid:</label>
        <div class="input-group col-sm-6">
            <input type="text" id="registrationkeyid" class="form-control" placeholder="If you have a GnuPG or PGP key then please enter its short key id here and we will print it on your badge." name="registration.keyid" />
        </div>
    </div>
% endif

    <div class="row form-group">
        <label for="registration.planetfeed" class="col-sm-4 control-label">Planet feed:</label>
        <div class="input-group col-sm-6">
            <input type="text" id="registrationplanetfeed" class="form-control" placeholder="If you have a blog and would like it included in the ${ h.event_name() } planet, please specify a feed URL" name="registration.planetfeed" />
        </div>
    </div>
    
    <div class="row form-group">
        <label for="registration.silly_description" class="col-sm-4 control-label">Description:</label>
        <blockquote class="blockquote-reverse col-sm-6">
            <p>${ c.silly_description }</p>
            <footer>This is a randomly chosen description for your name badge</footer>
        </blockquote>
        ${ h.hidden('registration.silly_description') }
        ${ h.hidden('registration.silly_description_checksum') }
    </div>

          </fieldset>
% endif
          <fieldset>
              <h2>Subscriptions</h2>
             <p class="note">Tick below to sign up for any of the following:</p>

            <p class="entries">
                <table class="table">
                  <tr>
                    <td>

                    <div class="checkbox">
                        <label>
                        <input type="checkbox" name="registration.signup.linuxaustralia" id="registrationsignuplinuxaustralia" value="1" >
                        Membership of Linux Australia. <a href="http://www.linux.org.au/" target="_blank">(read more)</a>
                        </label>
                    </div>
                    <div class="checkbox">
                        <label>
                        <input type="checkbox" name="registration.signup.announce" id="registrationsignupannounce" value="1" checked="checked">
                        The low traffic ${ h.event_name() }  announcement mailing list
                        </label>
                    </div>
                    <div class="checkbox">
                        <label>
                        <input type="checkbox" name="registration.signup.chat" id="registrationsignupchat" value="1" >
                        The ${ h.event_name() } attendees mailing list
                        </label>
                    </div>

                    </td>
                  </tr>
                </table>
            </p>
          </fieldset>