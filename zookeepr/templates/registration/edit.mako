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

        <p class="submit">${ h.submit('update','Update') }</p>
      ${ h.end_form() }

    </div>
