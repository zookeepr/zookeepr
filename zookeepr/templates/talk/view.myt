<h2><% c.talk.title |h %></h2>

<p>A <% c.talk.type.name %> by
% for p in c.talk.people:
<% h.link_to(p.fullname, url=h.url(controller='profile', action='view', id=p.id)) %>
% #endfor
</p>

% if c.signed_in_person in c.talk.people or (c.signed_in_person and 'organiser' in [x.name for x in c.signed_in_person.roles]):
    <% h.link_to('Edit', url=h.url(controller='proposal',action='edit',id=c.talk.id)) %>
% #endif
<div id="abstract">
#% content = h.wiki_here()
% content = h.wiki_fragment('/wiki/talk/%d' % c.talk.id)
% if 'This page does not exist yet.' in content:
<% c.talk.abstract |s %>
#<p><% h.link_to('Edit wiki', url=h.url('/talk/%d?action=edit' % c.talk.id)) %></p>
% else:
<% content %>
% #endif
</div>


<script type='text/javascript' src="/mv_embed.js"></script>

<div style="border:solid;width:320px;height:270px;overflow:hidden;" name="mv_embed">
       <!-- be sure to give the absolute address for the media url. This should be on the same domain as the script -->
       <input type="hidden" name="media_url" value="http://mirror.linux.org.au/pub/linux.conf.au/2007/video/talks/<% c.talk.id %>.ogg" />
       <input type="hidden" name="img_thumbnail" value="http://mirror.linux.org.au/pub/linux.conf.au/2007/video/talks/<% c.talk.id %>.jpg" />
</div>
 +<a href="http://mirror.linux.org.au/pub/linux.conf.au/2007/video/talks/<% c.talk.id %>.ogg">Direct link to video</a>
<!-- end embed lines -->



<%method title>
<% c.talk.title |h %> - <& PARENT:title &>
</%method>
