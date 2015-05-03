    <div id="flash">
<% messages = h.get_flashes() %>
%if messages:
%   for (category, msgs) in messages.iteritems():
      <div class="alert alert-info" role="alert">
%       if len(msgs) is 1:
            <p>${ msgs[0] | n }</p>
%       else:
            <ul>
%          for msg in msgs:
                <li>${ msg | n }</li>
%          endfor
            </ul>
%       endif
        </div>
%   endfor
%endif
%if c.form_errors:
        <div class="alert alert-danger" role="alert">
        <ul>
%       for field in c.form_errors:
           <li>
## To provide pretty field names pass them in via c.form_fields. 
%  if field in c.form_fields:
  ${ c.form_fields[field] }
%  else:
  ${ field }
%  endif
: ${ c.form_errors[field] | n }</li>
%       endfor
        </ul>
        </div>
%endif
    </div>
