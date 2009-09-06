        <p class="label"><label for="special_offerenabled">Enabled:</label> ${ h.checkbox('special_offer.enabled') }</p>

        <p class="label"><span class="mandatory">*</span><label for="special_offer.name">Name:</label></p>
        <p class="entries">${ h.text('special_offer.name') }</p>

        <p class="label"><span class="mandatory">*</span><label for="special_offer.description">Description and welcome message:</label></p>
        <p class="entries">${ h.textarea('special_offer.description', rows=10, cols=80) }</p>

        <p class="label"><span class="mandatory">*</span><label for="special_offer.id_name">Name of the ID they need to give us:</label></p>
        <p class="entries">${ h.text('special_offer.id_name') }</p>
