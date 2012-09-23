      <p>
        <label for="ceiling.parent">Parent Ceiling:</label>
        ${ h.select('ceiling.parent', None, [(ceiling.id, ceiling.name) for ceiling in c.ceilings], prompt="None") }
        (This ceiling will not become available until the parent is not available)
      <p>
        <label for="ceiling.name">Name:</label>
        ${ h.text('ceiling.name') }
      </p>

      <p>
        <label for="ceiling.max_sold">Ceiling Limit:</label>
        ${ h.text('ceiling.max_sold') }
      </p>

      <p>
        <label for="ceiling.available_from">Available From:</label>
        ${ h.text('ceiling.available_from') }
      </p>

      <p>
        <label for="ceiling.available_until">Available Until:</label>
        ${ h.text('ceiling.available_until') }
      </p>
      <h3><label for="ceiling.products">Products in this Ceiling</label></h3>
      <p>
        <select name="ceiling.products" multiple="multiple">
% for category in c.product_categories:
          <optgroup label="${ category.name }">
%   for product in category.products:
%       if c.ceiling:
            <option value="${ product.id }" selected="selected">${ product.description }</option>
%       else:
            <option value="${ product.id }">${ product.description }</option>
%       endif
%   endfor
          </optgroup>
% endfor
        </select>
      </p>
