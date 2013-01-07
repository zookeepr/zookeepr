      <h2>Add a voucher code</h2>

      <div>

        <fieldset>

          <p class="label"><span class="mandatory">*</span><label for="voucher.count">Count:</label></p>
          <p class="entries">${ h.text('voucher.count', size=5) }</p>
          <p class="note">How many voucher codes to generate.</p>

          <p class="label"><span class="mandatory">*</span><label for="voucher.leader">Group leader:</label></p>
          <p class="entries">${ h.text('voucher.leader', size=5) }</p>
          <p class="note">ID of person who should be given the codes and
          allowed to see who's using them, as per the
          ${ h.link_to('profile list', url=h.url_for(controller='person',
          action='index')) }. If nobody, use your own ID: ${
          h.signed_in_person().id }</p>

          <p class="label"><label for="voucher.code">Code prefix:</label></p>
          <p class="entries">${ h.text('voucher.code', size=40) }</p>
          <p class="note">If you enter "foo", it might generate "foo-ooH4epe7". If blank, it'll just generate "ooH4epe7". Theoretically it might be a good idea to avoid 1, l, I, 0 and O, but I'm not sure how else one would spell IBM or GOOGLE :-)</p>

          <p class="label"><span class="mandatory">*</span>Product Selections</p>
          <p class="entries">
          <table>
% for category in c.product_categories:
            <tr>
              <td colspan="4" align="center"><h3>${ category.name |h }</h3></td>
            </tr>
            <tr>
              <th>Product</th>
              <th>Price</th>
%       if category.display == 'radio':
              <th></th>
%       else:
              <th>Qty</th>
%       endif
              <th>% Discount</th>
            </tr>
%       for product in category.products_nonfree:
<%
            soldout = ''
            if not product.available():
                soldout = ' <span class="mandatory">SOLD&nbsp;OUT or UNAVAILABLE</span> '
%>

            <tr>
              <td><label for="products.product_${ product.id }">${ soldout | n}${ product.description }</label></td>
              <td>${ h.integer_to_currency(product.cost) }</td>
%           if category.display == 'radio':
              <td>${ h.radio('products.category_' + str(category.id), product.id) }
## TODO: Add other display options here later, not adding select because we want accom to include a qty
%           else:
              <td>${ h.text('products.product_' + str(product.id) + '_qty', size=3) }</td>
%           endif
%           if category.display == 'radio' and category.products_nonfree[0] == product:
              <td rowspan="${ len(category.products_nonfree.all()) }">${ h.text('products.category_' + str(category.id) + '_percentage', size=3) }</td>
%           elif category.display == 'radio':
              <!-- pass -->
%           else:
              <td>${ h.text('products.product_' + str(product.id) + '_percentage', size=3) }</td>
%           endif
            </tr>
%       endfor
% endfor
          </table>
          </p>
          <p class="note">Discount percent is Between 0 and 100</p>


          <p class="label"><span class="mandatory">*</span><label for="voucher.comment">Comment:</label></p>
          <p class="entries">${ h.text('voucher.comment', size=60) }</p>
          <p class="note">Why are they getting a voucher? <b>This will appear on the invoices</b> as the item description for the negative amount - phrase accordingly...</p>
        </fieldset>
      </div>
