        <p class="label"><span class="mandatory">*</span><label for="product_category.name">Name:</label></p>
        <p class="entries">${ h.text('product_category.name') }</p>

        <p class="label"><span class="mandatory">*</span><label for="product_category.description">Description:</label></p>
        <p class="entries">${ h.text('product_category.description') }</p>

        <p class="label"><label for="product_category.note">Note:</label></p>
        <p class="entries">${ h.text('product_category.note') }</p>

        <p class="label"><span class="mandatory">*</span><label for="product_category.display">Display as:</label></p>
        <p class="entries">
        ${ h.radio('product_category.display', 'radio', label="Radio button (single selection)") }
        <br />
        ${ h.radio('product_category.display', 'select', label="Drop down menu (single selection)") }
        <br />
        ${ h.radio('product_category.display', 'checkbox', label="Checkbox (multiple selection)") }
        <br />
        ${ h.radio('product_category.display', 'qty', label="Quantity (integer)") }
        </p>

        <p class="label"><label for="product_category.display_mode">Display mode:</label></p>
        <p class="entries">${ h.text('product_category.display_mode') }</p>

        <p class="label"><label for="product_category.display_order">Display Order:</label></p>
        <p class="entries">${ h.text('product_category.display_order') }</p>

        <p class="label"><label for="product_category.min_qty">Min. Quantity:</label></p>
        <p class="entries">${ h.text('product_category.min_qty') }</p>

        <p class="label"><label for="product_category.max_qty">Max. Quantity:</label></p>
        <p class="entries">${ h.text('product_category.max_qty') }</p>

        <p class="note"><span class="mandatory">*</span> - Mandatory field</p>
