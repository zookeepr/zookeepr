% import array
% subdirs = [ 'people', 'misc', 'location' ]
% subdirs = h.array_random( subdirs )

<div id="randoms">
% for dir in subdirs:
    <img src="<% h.random_pic( dir ) %>" alt="Random <% dir | h %>" height="100" width="100" title="Random <% dir | h %> image" /> 
% # end for
    <strong></strong>
</div>
