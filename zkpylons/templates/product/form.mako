      <p><label for="product.description">Description:</label><br>
      ${ h.text('product.description') }</p>

      <p>
        <label for="product.category">Category</label>
        <select id="product.category" name="product.category">
% for category in c.product_categories:
          <option value="${category.id}">${ category.name }</option>
% endfor
        </select>
      </p>

      <p>
        <label for="product.display_order">Display Order:</label>
        ${ h.text('product.display_order') }
      </p>

      <p>
        <label for="product.active">Active:</label>
        ${ h.checkbox('product.active') }
      </p>

      <p>
        <label for="product.cost">Cost (in cents. ie $100 = 10000):</label><br>
        ${ h.text('product.cost', size='10') }
      </p>

      <p>
        <label for="product.auth">Auth code:</label><br>
        ${ h.textarea('product.auth', cols=80, rows=5) }
      </p>

      <p>
        <label for="product.validate">Validate code:</label><br>
        ${ h.textarea('product.validate', cols=80, rows=5) }
      </p>

      <h3><label for="product.ceilings">This Products Ceilings</label></h3>
      <p>
        <select id="product.ceilings" name="product.ceilings" multiple="multiple">
% for ceiling in c.ceilings:
            <option value="${ ceiling.id }">${ ceiling.name }</option>
% endfor
        </select>
      </p>
