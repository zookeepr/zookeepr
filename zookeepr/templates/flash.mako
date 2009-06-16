    <div id="flash">
<% messages = h.get_flashes() %>
%if messages:
%   for (category, msgs) in messages.iteritems():
        <div class="message message-${ h.computer_title(category) }">
%       if len(msgs) is 1:
            <p>${ msgs[0] }</p>
%       else:
            <ul>
%          for msg in msgs:
                <li>${ msg }</li>
%          endfor
            </ul>
%       endif
        </div>
%   endfor
%endif
    </div>
