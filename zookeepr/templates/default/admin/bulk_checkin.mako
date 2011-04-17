${ h.form(h.url_for(), method='post') }
<p class="entries">IDs: ${ h.textarea('ids', cols=10, rows=10, tabindex=1) }</p>

<p class="entries">text: ${ h.text('note', size=30, tabindex=2, value='Here! (bulk)') }</p>

<p class="entries">time: ${ h.text('entered', size=20, tabindex=3, value=now) }</p>

<p class="submit">${ h.submit('submit', "Submit!") }</p>

${ h.end_form() }
