% import array
% subdirs = [ 'people', 'misc', 'location' ]
% subdirs = h.array_random( subdirs )

% if request.environ['HTTP_USER_AGENT'].find( 'MSIE 6' ) == -1:
<div id="randoms">
%   for dir in subdirs:
    <img src="<% h.random_pic( dir ) %>" alt="Random <% dir | h %>" height="100" width="100" title="Random <% dir | h %> image" /> 
%   # end for
    <strong></strong>
</div>
% # end if
