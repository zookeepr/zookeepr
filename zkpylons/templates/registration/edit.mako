<%inherit file="/base.mako" />
    <h1>Edit registration</h1>

    <div id="registration">

% if errors:
      <p class="error-message">There
%   if len(errors)==1:
      is one problem
%   else:
      are ${ `len(errors)` |h } problems
%   endif
      with your registration form, highlighted in red below. Please correct and re-submit.</p>
% endif

${ h.form(h.url_for()) }
<%include file="form.mako" />
        ${ h.hidden('special_offer.name', '') }
        ${ h.hidden('special_offer.member_number', '') }
        ${ h.hidden('person.i_agree', True) }
        <p class="submit">${ h.submit('submit','Update') } ${ h.link_to('back', url=h.url_for(action='status', id=None)) }</p>
      ${ h.end_form() }

    </div>
