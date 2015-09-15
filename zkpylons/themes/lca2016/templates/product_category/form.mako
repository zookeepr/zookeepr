	<div class="row form-group"> 
      <label for="product_categoryname" class="col-sm-2 control-label">Name: </label>
      <div class="input-group col-sm-10">
        <input class="form-control" id="product_categoryname" name="product_category.name" required></input>
        <span class="input-group-addon" id="basic-addon2">required</span>
      </div>
    </div>
<!--
        <p class="label"><span class="mandatory">*</span><label for="product_category.name">Name:</label></p>
        <p class="entries">${ h.text('product_category.name') }</p>
        -->

	<div class="row form-group"> 
      <div class="textarea">
        <label for="product_categorydescription" class="col-sm-2 control-label">Description: </label>
        <textarea class="form-control" id="product_categorydescription" placeholder="Description of category" name="product_category.description" rows="5" cols="80" required></textarea>
      </div>
    </div>
    
    <div class="row form-group"> 
      <div class="textarea">
        <label for="product_categorynote" class="col-sm-2 control-label">Note: </label>
        <textarea class="form-control" id="product_categorynote" placeholder="Category note" name="product_category.note" rows="5" cols="80"></textarea>
      </div>
    </div>

    <div class="row form-group">
      <label for="proposaltype" class="col-sm-2 control-label">Display as:</label>
      <div class="col-sm-10">
      
    	<div class="radio">
      		<label>
        	<input type="radio" name="product_category.display" id="product_category.display_radio" value="radio" checked="checked">
        	Radio button (single selection)
      		</label>
    	</div>
    	<div class="radio">
      		<label>
        	<input type="radio" name="product_category.display" id="product_category.display_select" value="select">
        	Drop down menu (single selection)
      		</label>
    	</div>
    	<div class="radio">
      		<label>
        	<input type="radio" name="product_category.display" id="product_category.display_checkbox" value="checkbox">
        	Checkbox (multiple selection)
      		</label>
    	</div>
    	<div class="radio">
      		<label>
        	<input type="radio" name="product_category.display" id="product_category.display_qty" value="qty">
        	Quantity (integer)
      		</label>
    	</div>
    	
      </div>
    </div>
<!--
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
        -->
        
	<div class="row form-group"> 
      <label for="product_categorydisplay_mode" class="col-sm-2 control-label">Display mode:</label>
      <div class="input-group col-sm-10">
        <input class="form-control" id="product_categorydisplay_mode" name="product_category.display_mode"></input>
      </div>
    </div>
    
    <div class="row form-group"> 
      <label for="product_categorydisplay_order" class="col-sm-2 control-label">Display order:</label>
      <div class="input-group col-sm-10">
        <input class="form-control" id="product_categorydisplay_order" name="product_category.display_order"></input>
      </div>
    </div>
    
    <div class="input-group">
      <div class="checkbox">
      <label>
        <input type="checkbox" id="product_categoryinvoice_free_products" name="product_category.invoice_free_products" value="1">
        Invoice free products
      </label>
      </div>
    </div>
    
    <div class="row form-group"> 
      <label for="product_categorymin_qty" class="col-sm-2 control-label">Min. Quantity:</label>
      <div class="input-group col-sm-10">
        <input class="form-control" id="product_categorymin_qty" name="product_category.min_qty" required></input>
        <span class="input-group-addon" id="basic-addon2">required</span>
      </div>
    </div>
    
    <div class="row form-group"> 
      <label for="product_categorymax_qty" class="col-sm-2 control-label">Max. Quantity:</label>
      <div class="input-group col-sm-10">
        <input class="form-control" id="product_categorymax_qty" name="product_category.max_qty" required></input>
        <span class="input-group-addon" id="basic-addon2">required</span>
      </div>
    </div>

