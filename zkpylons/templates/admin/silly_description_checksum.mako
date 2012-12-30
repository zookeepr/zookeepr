<%inherit file="/base.mako" />
${ h.form(h.url_for(), method='get') }
<p class="entries">Silly Description: ${ h.text('silly_description', size=60, tabindex=1) }</p>
${ h.end_form() }

%if c.silly_description_checksum:
<p>Checksum for: ${ c.silly_description }</p>
<p>is: ${ c.silly_description_checksum }</p>
%endif
